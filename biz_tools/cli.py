"""CLI interface for hermes-biz-tools."""

import json
import sys
from pathlib import Path

import click

from . import __version__
from .generators import ContentGenerator, generate_room_card_pdf
from .templates_loader import TEMPLATES


@click.group()
@click.version_option(__version__)
def main():
    """Hermes Biz Tools - AI marketing content generator for Chinese small businesses."""


@main.command()
@click.option("--name", required=True, help="Business/B&B name")
@click.option("--type", "biz_type", default="民宿", help="Business type")
@click.option("--room-type", default="海景大床房", help="Room type for room card")
@click.option("--price", default="¥XXX", help="Price per night")
@click.option("--features", default="一线海景,干净卫生,免费WiFi", help="Comma-separated features")
@click.option("--style", default="warm", type=click.Choice(["warm", "professional", "promotion"]))
@click.option("--output", "-o", default="output", help="Output directory")
@click.option("--all", "generate_all", is_flag=True, help="Generate all content types")
def generate(name, biz_type, room_type, price, features, style, output, generate_all):
    """Generate marketing content for your business."""
    gen = ContentGenerator(output)
    features_list = [f.strip() for f in features.split(",")]

    results = []

    if generate_all:
        # Room card
        path = gen.room_card(name, room_type, price, features_list)
        results.append(("房型卡", path))

        # WeChat posts
        posts = gen.wechat_post(name, biz_type, style)
        for i, post in enumerate(posts):
            p = Path(output) / f"wechat_post_{i+1}.md"
            p.write_text(post, encoding="utf-8")
            results.append((f"朋友圈文案(版{i+1})", str(p)))

        # Xiaohongshu
        path = gen.xiaohongshu(name, "南澳岛青澳湾", features_list)
        results.append(("小红书笔记", path))

        # Flyer
        flyer_content = "\n".join([
            f"🌟 {name} 限时优惠中！",
            "",
            f"🏠 {room_type}：{price}/晚",
            *[f"✅ {f}" for f in features_list],
            "",
            "📲 扫码预订享专属折扣",
        ])
        path = gen.flyer(name, f"{name} · 限时特惠", flyer_content)
        results.append(("促销传单", path))

        # Weekly pack
        pack = gen.weekly_pack(name, biz_type)
        p = Path(output) / "weekly_plan.json"
        p.write_text(json.dumps(pack, ensure_ascii=False, indent=2), encoding="utf-8")
        results.append(("周运营计划", str(p)))

    else:
        # Default: room card only
        path = gen.room_card(name, room_type, price, features_list)
        results.append(("房型卡", path))

    click.echo("\n✅ 生成完成!\n")
    for label, path in results:
        click.echo(f"  📄 {label}: {path}")

    click.echo(f"\n📁 输出目录: {Path(output).resolve()}")


@main.command()
def templates():
    """List available built-in templates."""
    click.echo("\n📋 可用模板:\n")
    for name, info in TEMPLATES.items():
        click.echo(f"  {name}: {info.get('desc', '')}")
    click.echo()


@main.command()
@click.argument("md_file")
@click.option("--output", "-o", default=None, help="PDF output path")
def convert(md_file, output):
    """Convert room card Markdown to PDF."""
    try:
        pdf_path = generate_room_card_pdf(md_file, output)
        click.echo(f"✅ PDF 已生成: {pdf_path}")
    except Exception as e:
        click.echo(f"❌ 转换失败: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()

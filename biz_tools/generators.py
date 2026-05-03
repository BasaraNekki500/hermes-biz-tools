"""Core generators: room card, WeChat post, Xiaohongshu note, flyer."""

import json
import os
import textwrap
from datetime import datetime
from pathlib import Path


class ContentGenerator:
    """Generate marketing content from templates + structured data."""

    def __init__(self, output_dir: str = "output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    # ── Room Card ──────────────────────────────────────────────

    def room_card(self, name: str, room_type: str, price: str,
                  features: list, description: str = "") -> str:
        """Generate WeChat-optimized room card markdown."""
        features_bullets = "\n".join(f"✅ {f}" for f in features)
        timestamp = datetime.now().strftime("%Y-%m-%d")

        content = f"""# 🏠 {name} · {room_type}

**💰 价格：{price}/晚**

---

## ✨ 特色亮点

{features_bullets}

---

## 📝 详情

{description or f'{room_type}，舒适温馨，适合{price.split("¥")[-1] if "¥" in price else ""}预算的旅客。'}

---

*生成时间：{timestamp}*
*宝缦美宿 · 南澳岛青澳湾*
"""
        path = self.output_dir / f"room_card_{room_type}.md"
        path.write_text(content, encoding="utf-8")
        return str(path)

    # ── WeChat Moments Copy ────────────────────────────────────

    def wechat_post(self, name: str, business_type: str,
                    style: str = "warm") -> list:
        """Generate 3 WeChat朋友圈 copy variants."""
        templates = {
            "warm": [
                f"🏡 在南澳岛，我找到了一个叫「{name}」的地方。\n\n"
                f"推开窗就是海，空气中带着咸咸的味道。\n"
                f"老板亲自打理的民宿，每个角落都透着用心。\n\n"
                f"如果你也想来南澳吹吹海风，这里值得住一晚 🌊\n"
                f"📍 南澳县青澳湾\n"
                f"#南澳岛民宿 #{name}",

                f"🌅 早晨是被海浪声叫醒的。\n\n"
                f"在{name}的第三天，终于学会了慢下来。\n"
                f"一杯咖啡，一片海，一本书——\n"
                f"这就是我想要的生活啊。\n\n"
                f"📌 私信预订享粉丝优惠哦～\n"
                f"#海岛慢生活 #南澳旅游",

                f"💡 {name}入住体验分享\n\n"
                f"✔ 位置：青澳湾海边，步行3分钟到沙滩\n"
                f"✔ 房间：干净宽敞，海景房视野绝了\n"
                f"✔ 服务：老板超热情，还推荐了本地海鲜\n\n"
                f"五一出游的宝子们可以冲！\n"
                f"👉 戳我获取预订链接\n"
                f"#民宿推荐 #南澳岛旅游攻略",
            ],
            "professional": [
                f"【{name} · 民宿运营日志】\n\n"
                f"今日满房 ✅\n"
                f"感谢每一位客人的信任与选择。\n\n"
                f"我们始终坚持以品质服务为核心，\n"
                f"为每一位旅人提供舒适、温馨的住宿体验。\n\n"
                f"📍 汕头南澳县青澳湾\n"
                f"📞 预订咨询请私信",

                f"🏆 {name}\n\n"
                f"青澳湾优质民宿推荐 | 品质住宿之选\n\n"
                f"• 一线海景 • 温馨舒适\n"
                f"• 专业服务 • 性价比高\n\n"
                f"欢迎团队/家庭出游预订\n"
                f"长期合作可享协议价",

                f"📊 {name} 本周运营简报\n\n"
                f"入住率：XX%\n"
                f"好评率：98%\n"
                f"新客占比：XX%\n\n"
                f"感谢新老客人的支持，\n"
                f"我们会继续努力提升服务质量！\n\n"
                f"#民宿运营 #南澳住宿",
            ],
            "promotion": [
                f"🎉 {name} 限时特惠！\n\n"
                f"即日起预订享 **{business_type}专属折扣**\n"
                f"🔥 前10位预订送精美伴手礼\n\n"
                f"🌟 为什么选择我们？\n"
                f"✅ 一线海景房  ✅ 贴心管家服务\n"
                f"✅ 免费攻略咨询  ✅ 本地海鲜代订\n\n"
                f"👇 扫码预订锁定优惠\n"
                f"名额有限，先到先得！",

                f"⚡ 捡漏！{name} 今日空房\n\n"
                f"临时退订放出：\n"
                f"🛏 海景大床房 × 1\n"
                f"🛏 亲子家庭房 × 1\n\n"
                f"今晚入住 → 直接**8折**\n"
                f"手慢无！私信秒回 🔥",

                f"🎁 {name} × 五一宠粉福利\n\n"
                f"转发本条朋友圈 → 抽 **免费住宿一晚**\n\n"
                f"参与方式：\n"
                f"① 关注并点赞\n"
                f"② 转发到朋友圈\n"
                f"③ 截图私信即可\n\n"
                f"开奖时间：本周日20:00\n"
                f"#福利 #南澳岛旅行",
            ],
        }
        return templates.get(style, templates["warm"])

    # ── Xiaohongshu Note ──────────────────────────────────────

    def xiaohongshu(self, name: str, location: str, highlights: list,
                    tips: list = None) -> str:
        """Generate Xiaohongshu-style note with hashtags."""
        highlights_str = "\n".join(f"🌟 {h}" for h in highlights)
        tips_str = "\n".join(f"💡 {t}" for t in (tips or ["提前预订优惠多", "淡季出行体验更佳"]))
        tags = ["南澳岛", "民宿推荐", "汕头旅游", "海岛度假",
                "五一去哪玩", "广东周边游", name]

        content = f"""# 藏在{location}的宝藏{name}🏡 ｜ 真实入住体验

---

## 📍 位置

位于{location}，步行即可到达海边，交通便利，停车方便。

## ✨ 亮点

{highlights_str}

## 📝 入住感受

房间干净整洁，装修风格温馨舒适。
老板服务态度超级好，还推荐了当地特色美食。
窗外就是海景，早晨醒来心情超好～
性价比很高，适合情侣/家庭出游。

## 💡 小贴士

{tips_str}

---

📌 收藏起来下次去用～

{" ".join(f"#{t}" for t in tags)}
"""
        path = self.output_dir / f"xiaohongshu_{name}.md"
        path.write_text(content, encoding="utf-8")
        return str(path)

    # ── Flyer / Promo PDF (Markdown output) ───────────────────

    def flyer(self, name: str, title: str, content: str,
              contact: str = "私信咨询") -> str:
        """Generate promotional flyer in markdown."""
        timestamp = datetime.now().strftime("%Y-%m-%d")

        md = f"""# {title}

## {name}

{content}

---

📞 **联系方式**：{contact}
📍 **地址**：汕头南澳县青澳湾
🕐 **生成时间**：{timestamp}
"""
        path = self.output_dir / f"flyer_{name}.md"
        path.write_text(md, encoding="utf-8")
        return str(path)

    # ── Weekly Content Pack ────────────────────────────────────

    def weekly_pack(self, name: str, business_type: str) -> dict:
        """Generate a full week of content."""
        days = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
        themes = [
            "入住实拍分享",
            "周边景点推荐",
            "客人好评截图",
            "房型介绍专场",
            "周末特惠活动",
            "本地美食推荐",
            "下周预告 & 粉丝互动",
        ]
        pack = {}
        for day, theme in zip(days, themes):
            pack[day] = {
                "theme": theme,
                "copy": self.wechat_post(name, business_type, "warm")[0],
            }
        return pack


def generate_room_card_pdf(md_path: str, pdf_path: str = None) -> str:
    """Convert room card markdown to PDF (lightweight, no Hermes Agent needed)."""
    from fpdf import FPDF

    pdf = FPDF()
    pdf.add_page()
    pdf.add_font("NotoSansSC", "", "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc", uni=True)
    pdf.set_font("NotoSansSC", "", 12)

    content = Path(md_path).read_text(encoding="utf-8")
    for line in content.split("\n"):
        if line.startswith("# "):
            pdf.set_font("NotoSansSC", "", 20)
            pdf.cell(0, 15, line[2:])
            pdf.ln()
            pdf.set_font("NotoSansSC", "", 12)
        elif line.startswith("## "):
            pdf.set_font("NotoSansSC", "", 16)
            pdf.cell(0, 10, line[3:])
            pdf.ln()
            pdf.set_font("NotoSansSC", "", 12)
        elif line.strip():
            pdf.multi_cell(0, 8, line)
        else:
            pdf.ln(4)

    pdf_path = pdf_path or md_path.replace(".md", ".pdf")
    pdf.output(pdf_path)
    return pdf_path

# Hermes Biz Tools 🚀

> 面向小商家/民宿/个体户的 **AI 营销内容自动化工具链**
> 基于 Hermes Agent，一键生成微信/小红书/抖音营销素材

## 解决的问题

- ❌ 不会写文案？→ 一键生成朋友圈/小红书/公众号文案
- ❌ 不会做图？→ 自动生成房型卡/促销海报/宣传单 PDF
- ❌ 没时间运营？→ 定时批量生成，Cronjob 自动发布

## 快速开始

```bash
# 安装
pip install hermes-biz-tools

# 一键生成民宿营销全套
biz-tools generate --type all --business 民宿 --name "宝缦美宿"
```

## 功能

| 命令 | 输出 | 适用场景 |
|------|------|----------|
| `biz-tools generate wechat-post` | 朋友圈文案(3版) | 日常营销 |
| `biz-tools generate room-card` | 房型卡 PDF | 房型展示 |
| `biz-tools generate xiaohongshu` | 小红书笔记(含标签) | 种草引流 |
| `biz-tools generate flyer` | 促销传单 PDF | 节假日活动 |
| `biz-tools batch weekly` | 一周内容包 | 批量运营 |

## 赞助

如果这个工具帮你省了时间，欢迎赞助支持持续开发：

[💖 赞助本项目](https://github.com/sponsors/BasaraNekki500)

## License

MIT © BasaraNekki500

EMOJI_MAP = {

    ":smile:": "😄",
    ":laugh:": "😂",
    ":heart:": "❤️",
    ":love:": "😍",
    ":sad:": "😢",
    ":angry:": "😡",
    ":wink:": "😉",
    ":cool:": "😎",
    ":cry:": "😭",
    ":fire:": "🔥",
    ":thumbsup:": "👍",
    ":thumbsdown:": "👎",
    ":ok:": "👌",
    ":clap:": "👏",
    ":pray:": "🙏",
    ":party:": "🥳",
    ":rocket:": "🚀",
    ":star:": "⭐",
    ":check:": "✅",
    ":warning:": "⚠️",
    ":coffee:": "☕",
    ":gift:": "🎁",
    ":cake:": "🎂"
}


def convert_emojis(message):

    for shortcode, emoji in EMOJI_MAP.items():

        message = message.replace(
            shortcode,
            emoji
        )

    return message
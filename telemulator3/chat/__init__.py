"""Package for Telegram chats stuff."""


class Type:
    """Types of Telegram chats."""

    Private = 'private'
    Group = 'group'
    Supergroup = 'supergroup'
    Channel = 'channel'


class MemberStatus:
    """Status of Telegram chat member."""

    Creator = "creator"
    Administrator = "administrator"
    Member = "member"
    Restricted = "restricted"
    Left = "left"

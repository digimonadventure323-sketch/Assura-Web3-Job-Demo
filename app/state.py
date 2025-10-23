import reflex as rx
from typing import TypedDict
import random
import time


class TokenMetrics(TypedDict):
    total_supply: int
    circulating_supply: int
    total_staked: int
    total_unstaking: int
    total_burned: int


class PriceData(TypedDict):
    name: str
    price: float


class Suggestion(TypedDict):
    id: int
    type: str
    name: str
    title: str
    tags: list[str]
    avatar: str


class Proposal(TypedDict):
    id: int
    title: str
    description: str
    votes: int
    threshold: int
    status: str


class UserProfile(TypedDict):
    name: str
    portfolio: str
    hash: str
    staking_level: str
    avatar: str


class AppState(rx.State):
    """The main application state."""

    tabs: list[str] = [
        "Dashboard",
        "Chat & Community",
        "Wallet & Staking",
        "Projects",
        "Profile",
    ]
    active_tab: str = "Dashboard"
    is_dark_mode: bool = False
    is_mobile_menu_open: bool = False
    is_chat_modal_open: bool = False
    is_profile_modal_open: bool = False
    token_metrics: TokenMetrics = {
        "total_supply": 1000000000,
        "circulating_supply": 994550000,
        "total_staked": 4520000,
        "total_unstaking": 120000,
        "total_burned": 1250000,
    }
    price_chart_data: list[PriceData] = [
        {"name": "Day 1", "price": 0.015},
        {"name": "Day 2", "price": 0.018},
        {"name": "Day 3", "price": 0.017},
        {"name": "Day 4", "price": 0.021},
        {"name": "Day 5", "price": 0.025},
        {"name": "Day 6", "price": 0.023},
        {"name": "Day 7", "price": 0.028},
    ]
    suggestions: list[Suggestion] = []
    selected_profile: UserProfile | None = None
    community_view: str = "Chat"
    proposals: list[Proposal] = []

    @rx.event
    async def on_load(self):
        from app.states.wallet_state import WalletState

        if not self.suggestions:
            self._initialize_suggestions()
        if not self.proposals:
            self._initialize_proposals()
        wallet_sub_state = await self.get_state(WalletState)
        if not wallet_sub_state.transactions:
            wallet_sub_state._initialize_transactions()

    def _initialize_suggestions(self):
        """Helper to create initial suggestion data."""
        names = [
            "Alex",
            "Jordan",
            "Taylor",
            "Morgan",
            "Casey",
            "Riley",
            "Jessie",
            "Jamie",
            "Kai",
            "Rowan",
        ]
        skills = [
            "Smart Contract Dev",
            "UI/UX Designer",
            "Frontend Dev",
            "Backend Dev",
            "DevOps Engineer",
        ]
        projects = [
            "DeFi Platform",
            "NFT Marketplace",
            "DAO Tooling",
            "Web3 Game",
            "Wallet App",
        ]
        tags = [
            ["Solidity", "DeFi"],
            ["Figma", "Web3"],
            ["React", "Ethers.js"],
            ["Node.js", "API"],
            ["CI/CD", "Security"],
        ]
        for i in range(20):
            user_name = random.choice(names)
            if i % 2 == 0:
                self.suggestions.append(
                    {
                        "id": i,
                        "type": "worker",
                        "name": user_name,
                        "title": random.choice(skills),
                        "tags": random.choice(tags),
                        "avatar": f"https://api.dicebear.com/9.x/initials/svg?seed={user_name}",
                    }
                )
            else:
                self.suggestions.append(
                    {
                        "id": i,
                        "type": "project",
                        "name": f"Project by {user_name}",
                        "title": random.choice(projects),
                        "tags": random.choice(tags),
                        "avatar": f"https://api.dicebear.com/9.x/notionists/svg?seed={user_name}",
                    }
                )

    def _initialize_proposals(self):
        self.proposals = [
            {
                "id": 101,
                "title": "Add New Staking Tier: Platinum",
                "description": "Proposal to add a new top-tier staking level with higher rewards.",
                "votes": 47000,
                "threshold": 50000,
                "status": "voting",
            },
            {
                "id": 102,
                "title": "Increase Project Dispute Fee",
                "description": "Increase the dispute fee from 50 ASRA to 100 ASRA to prevent spam.",
                "votes": 62000,
                "threshold": 50000,
                "status": "passed",
            },
            {
                "id": 103,
                "title": "Community Grant for Dev Tooling",
                "description": "Fund a project to build better developer tools for the Assura ecosystem.",
                "votes": 35000,
                "threshold": 60000,
                "status": "voting",
            },
            {
                "id": 104,
                "title": "Marketing Campaign for Q3",
                "description": "Allocate funds for a major marketing push to attract new users.",
                "votes": 88000,
                "threshold": 75000,
                "status": "executed",
            },
        ]

    @rx.event
    def toggle_dark_mode(self):
        self.is_dark_mode = not self.is_dark_mode

    @rx.event
    def set_active_tab(self, tab_name: str):
        self.active_tab = tab_name
        self.is_mobile_menu_open = False

    @rx.event
    def set_community_view(self, view: str):
        self.community_view = view

    @rx.event
    def vote_on_proposal(self, proposal_id: int):
        for i, p in enumerate(self.proposals):
            if p["id"] == proposal_id:
                self.proposals[i]["votes"] += random.randint(100, 1000)
                break
        yield rx.toast(
            "Vote Cast!", description="Your vote has been recorded.", duration=3000
        )

    @rx.event
    def toggle_mobile_menu(self):
        self.is_mobile_menu_open = not self.is_mobile_menu_open

    @rx.event
    def refresh_metrics(self):
        """Simulates refreshing token metrics and chart data."""
        self.token_metrics["circulating_supply"] += random.randint(-10000, 10000)
        self.token_metrics["total_staked"] += random.randint(1000, 5000)
        self.token_metrics["total_unstaking"] = random.randint(5000, 20000)
        new_price_data = self.price_chart_data
        last_price = new_price_data[-1]["price"]
        new_price = last_price * (1 + random.uniform(-0.1, 0.1))
        new_day_num = len(new_price_data) + 1
        new_price_data.append(
            {"name": f"Day {new_day_num}", "price": round(new_price, 3)}
        )
        if len(new_price_data) > 10:
            new_price_data.pop(0)
        self.price_chart_data = new_price_data

    @rx.event
    def open_chat_modal(self):
        self.is_chat_modal_open = True

    @rx.event
    def close_chat_modal(self):
        self.is_chat_modal_open = False

    @rx.event
    def open_profile_modal(self, suggestion: Suggestion):
        self.selected_profile = {
            "name": suggestion["name"],
            "portfolio": "https://example.com/portfolio",
            "hash": f"0x{random.randbytes(32).hex()}",
            "staking_level": random.choice(["Silver", "Gold", "Diamond"]),
            "avatar": suggestion["avatar"],
        }
        self.is_profile_modal_open = True

    @rx.event
    def close_profile_modal(self):
        self.is_profile_modal_open = False
        self.selected_profile = None

    @rx.event
    def handle_form_submit(self, form_data: dict):
        yield rx.toast(
            "Form Submitted!",
            description="Your submission has been received.",
            duration=3000,
        )
import reflex as rx
from typing import TypedDict, Literal
import random
from app.states.wallet_state import Transaction

ProfileView = Literal["Worker", "Client"]


class PortfolioItem(TypedDict):
    title: str
    description: str
    image_url: str


class ProfileState(rx.State):
    profile_view: ProfileView = "Worker"
    expanded_sections: dict[str, bool] = {
        "portfolio": True,
        "job_history": False,
        "tx_history": False,
        "posted_projects": True,
    }
    worker_rating: float = 4.9
    worker_rank: int = 12
    completed_jobs: int = 34
    portfolio_items: list[PortfolioItem] = []
    client_projects_posted: int = 8
    client_total_spending: int = 120500
    client_dao_votes: int = 42
    transaction_history: list[Transaction] = []

    @rx.event
    def on_load(self):
        if not self.portfolio_items:
            self._initialize_profile_data()

    def _initialize_profile_data(self):
        self.portfolio_items = [
            {
                "title": "DeFi Dashboard",
                "description": "A comprehensive analytics dashboard for a lending protocol.",
                "image_url": "/placeholder.svg",
            },
            {
                "title": "NFT Minting Site",
                "description": "Frontend for a generative art NFT collection.",
                "image_url": "/placeholder.svg",
            },
        ]
        if not self.transaction_history:
            import datetime

            types: list[Literal["Deposit", "Withdraw", "Swap", "Stake", "Unstake"]] = [
                "Deposit",
                "Withdraw",
                "Swap",
                "Stake",
                "Unstake",
            ]
            statuses: list[Literal["Completed", "Pending", "Failed"]] = [
                "Completed",
                "Pending",
                "Failed",
            ]
            for i in range(10):
                tx_type = random.choice(types)
                amount_val = random.uniform(10, 1000)
                if tx_type == "Swap":
                    amount_str = (
                        f"{amount_val:.2f} USDT -> {amount_val * 45.5:.2f} ASRA"
                    )
                elif tx_type in ["Stake", "Unstake"]:
                    amount_str = f"{amount_val * 10:.2f} ASRA"
                else:
                    amount_str = f"${amount_val:.2f}"
                self.transaction_history.append(
                    {
                        "id": str(i + 1),
                        "type": tx_type,
                        "status": random.choice(statuses),
                        "date": (
                            datetime.date.today()
                            - datetime.timedelta(days=random.randint(1, 30))
                        ).strftime("%Y-%m-%d"),
                        "amount": amount_str,
                        "hash": f"0x{random.randbytes(32).hex()[:12]}...",
                    }
                )

    @rx.event
    def set_profile_view(self, view: ProfileView):
        self.profile_view = view

    @rx.event
    def toggle_section(self, section: str):
        self.expanded_sections[section] = not self.expanded_sections.get(section, False)

    @rx.event
    def download_job_id(self):
        yield rx.toast(
            "Download Started",
            description="Simulating JobID file download...",
            duration=3000,
        )
import reflex as rx
from typing import TypedDict, Literal
import datetime
import random


class Transaction(TypedDict):
    id: str
    type: Literal["Deposit", "Withdraw", "Swap", "Stake", "Unstake"]
    status: Literal["Completed", "Pending", "Failed"]
    date: str
    amount: str
    hash: str


class WalletState(rx.State):
    """State for managing wallet and staking."""

    wallet_view: str = "Wallet"
    usdt_balance: float = 1250.75
    asra_balance: float = 54320.5
    staked_asra: float = 25000.0
    staking_tier: str = "Gold"
    staking_rewards: float = 1250.25
    days_remaining: int = 45
    is_deposit_modal_open: bool = False
    is_withdraw_modal_open: bool = False
    is_swap_modal_open: bool = False
    is_stake_modal_open: bool = False
    is_unstake_modal_open: bool = False
    transaction_hash: str = ""
    transactions: list[Transaction] = []

    def _initialize_transactions(self):
        if self.transactions:
            return
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
                amount_str = f"{amount_val:.2f} USDT -> {amount_val * 45.5:.2f} ASRA"
            elif tx_type in ["Stake", "Unstake"]:
                amount_str = f"{amount_val * 10:.2f} ASRA"
            else:
                amount_str = f"${amount_val:.2f}"
            self.transactions.append(
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
    def set_wallet_view(self, view: str):
        self.wallet_view = view
        if not self.transactions:
            self._initialize_transactions()

    @rx.event
    def open_deposit_modal(self):
        self.is_deposit_modal_open = True
        self.transaction_hash = ""

    @rx.event
    def close_deposit_modal(self):
        self.is_deposit_modal_open = False

    @rx.event
    def open_withdraw_modal(self):
        self.is_withdraw_modal_open = True
        self.transaction_hash = ""

    @rx.event
    def close_withdraw_modal(self):
        self.is_withdraw_modal_open = False

    @rx.event
    def open_swap_modal(self):
        self.is_swap_modal_open = True
        self.transaction_hash = ""

    @rx.event
    def close_swap_modal(self):
        self.is_swap_modal_open = False

    @rx.event
    def open_stake_modal(self):
        self.is_stake_modal_open = True
        self.transaction_hash = ""

    @rx.event
    def close_stake_modal(self):
        self.is_stake_modal_open = False

    @rx.event
    def open_unstake_modal(self):
        self.is_unstake_modal_open = True
        self.transaction_hash = ""

    @rx.event
    def close_unstake_modal(self):
        self.is_unstake_modal_open = False

    @rx.event
    def mock_transaction(self, form_data: dict):
        self.transaction_hash = f"0x{random.randbytes(32).hex()}"
        yield rx.toast(
            "Transaction Submitted",
            description="Your transaction is being processed.",
            duration=4000,
        )
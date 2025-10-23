import reflex as rx
from app.state import AppState, Suggestion, Proposal
from app.states.chat_state import ChatState, Message


def header() -> rx.Component:
    return rx.el.header(
        rx.el.div(
            rx.el.div(
                rx.icon("layers", class_name="h-8 w-8 text-teal-400"),
                rx.el.span("Assura", class_name="text-2xl font-bold text-white"),
                class_name="flex items-center gap-3",
            ),
            rx.el.div(
                rx.el.nav(
                    rx.foreach(AppState.tabs, lambda item: nav_item(item)),
                    class_name="hidden md:flex items-center gap-2",
                ),
                rx.el.div(
                    rx.el.button(
                        rx.icon(
                            rx.cond(AppState.is_dark_mode, "sun", "moon"),
                            class_name="h-5 w-5",
                        ),
                        on_click=AppState.toggle_dark_mode,
                        class_name="p-2 rounded-full hover:bg-gray-700/50 transition-colors",
                    ),
                    rx.el.button(
                        rx.icon("menu", class_name="h-6 w-6"),
                        on_click=AppState.toggle_mobile_menu,
                        class_name="p-2 rounded-md md:hidden hover:bg-gray-700/50 transition-colors",
                    ),
                    class_name="flex items-center gap-2 text-white",
                ),
                class_name="flex items-center gap-4",
            ),
            class_name="flex items-center justify-between h-16 px-4 md:px-6",
        ),
        rx.cond(
            AppState.is_mobile_menu_open,
            rx.el.nav(
                rx.el.nav(
                    rx.foreach(AppState.tabs, lambda item: mobile_nav_item(item)),
                    class_name="flex flex-col gap-2 pt-2 pb-4",
                ),
                class_name="md:hidden bg-gray-800/50 backdrop-blur-sm px-4",
            ),
            None,
        ),
        class_name="sticky top-0 z-50 border-b border-gray-700/50 bg-gray-900/50 backdrop-blur-lg font-['Lato']",
    )


def nav_item(text: str) -> rx.Component:
    return rx.el.a(
        rx.el.p(
            text,
            class_name=rx.cond(
                AppState.active_tab == text,
                "text-teal-400 font-semibold",
                "text-gray-300 hover:text-white transition-colors",
            ),
        ),
        on_click=lambda: AppState.set_active_tab(text),
        class_name="px-3 py-2 rounded-md text-sm cursor-pointer",
    )


def mobile_nav_item(text: str) -> rx.Component:
    return rx.el.a(
        rx.el.p(
            text,
            class_name=rx.cond(
                AppState.active_tab == text,
                "text-teal-300 bg-teal-900/50",
                "text-gray-200 hover:bg-gray-700/50",
            ),
        ),
        on_click=lambda: AppState.set_active_tab(text),
        class_name="block px-3 py-2 rounded-md text-base font-medium cursor-pointer transition-colors",
    )


from app.states.wallet_state import WalletState, Transaction
from app.states.projects_state import ProjectsState, Project
from app.states.profile_state import ProfileState


def main_content() -> rx.Component:
    return rx.el.main(
        rx.match(
            AppState.active_tab,
            ("Dashboard", dashboard_page()),
            ("Chat & Community", chat_community_page()),
            ("Wallet & Staking", wallet_staking_page()),
            ("Projects", projects_page()),
            ("Profile", profile_page()),
            rx.el.div(
                rx.el.p(f"Content for {AppState.active_tab}", class_name="text-2xl"),
                class_name="flex items-center justify-center h-96",
            ),
        ),
        class_name=rx.cond(
            AppState.is_dark_mode,
            "bg-gray-900 text-gray-200",
            "bg-gray-100 text-gray-800",
        ),
    )


def dashboard_page() -> rx.Component:
    return rx.el.div(
        token_metrics_panel(),
        rx.el.div(
            rx.el.div(form_panel(), class_name="lg:col-span-1 space-y-6"),
            rx.el.div(suggestion_feed(), class_name="lg:col-span-2"),
            class_name="grid grid-cols-1 lg:grid-cols-3 gap-6",
        ),
        chat_modal(),
        profile_modal(),
        class_name="p-4 md:p-6 space-y-6",
    )


def wallet_staking_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1("Wallet & Staking", class_name="text-3xl font-bold"),
            wallet_staking_toggle(),
            class_name="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-6",
        ),
        rx.match(
            WalletState.wallet_view,
            ("Wallet", wallet_view()),
            ("Staking", staking_view()),
        ),
        class_name="p-4 md:p-6",
    )


def wallet_staking_toggle() -> rx.Component:
    return rx.el.div(
        rx.el.button(
            "Wallet",
            on_click=lambda: WalletState.set_wallet_view("Wallet"),
            class_name=rx.cond(
                WalletState.wallet_view == "Wallet",
                "px-4 py-2 rounded-l-lg bg-teal-600 text-white font-semibold",
                "px-4 py-2 rounded-l-lg bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600",
            ),
        ),
        rx.el.button(
            "Staking",
            on_click=lambda: WalletState.set_wallet_view("Staking"),
            class_name=rx.cond(
                WalletState.wallet_view == "Staking",
                "px-4 py-2 rounded-r-lg bg-teal-600 text-white font-semibold",
                "px-4 py-2 rounded-r-lg bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600",
            ),
        ),
        class_name="flex",
    )


def wallet_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            balance_card("USDT Balance", WalletState.usdt_balance, "$"),
            balance_card("ASRA Balance", WalletState.asra_balance, "ASRA"),
            class_name="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6",
        ),
        rx.el.div(
            rx.el.button(
                "Deposit",
                on_click=WalletState.open_deposit_modal,
                class_name="wallet-button",
            ),
            rx.el.button(
                "Withdraw",
                on_click=WalletState.open_withdraw_modal,
                class_name="wallet-button",
            ),
            rx.el.button(
                "Swap", on_click=WalletState.open_swap_modal, class_name="wallet-button"
            ),
            class_name="flex items-center gap-4 mb-8",
        ),
        transaction_history(),
        deposit_modal(),
        withdraw_modal(),
        swap_modal(),
        class_name="max-w-7xl mx-auto w-full",
    )


def balance_card(title: str, balance: rx.Var[float], currency: str) -> rx.Component:
    return rx.el.div(
        rx.el.p(title, class_name="text-sm text-gray-400"),
        rx.el.p(f"{balance.to_string()} {currency}", class_name="text-3xl font-bold"),
        class_name="p-6 rounded-xl shadow-md border "
        + rx.cond(
            AppState.is_dark_mode,
            "bg-gray-800 border-gray-700",
            "bg-white border-gray-200",
        ),
    )


def transaction_history() -> rx.Component:
    return rx.el.div(
        rx.el.h2("Transaction History", class_name="text-2xl font-bold mb-4"),
        rx.el.div(
            rx.el.div(
                rx.el.div("Type", class_name="transaction-header"),
                rx.el.div("Amount", class_name="transaction-header hidden md:block"),
                rx.el.div("Date", class_name="transaction-header hidden md:block"),
                rx.el.div("Status", class_name="transaction-header"),
                rx.el.div("Hash", class_name="transaction-header hidden lg:block"),
                class_name="hidden md:grid grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4 px-6 py-3 border-b "
                + rx.cond(
                    AppState.is_dark_mode,
                    "border-gray-700 bg-gray-800",
                    "border-gray-200 bg-gray-50",
                ),
            ),
            rx.foreach(WalletState.transactions, transaction_row),
            class_name="rounded-xl border overflow-hidden "
            + rx.cond(AppState.is_dark_mode, "border-gray-700", "border-gray-200"),
        ),
    )


def transaction_row(tx: Transaction) -> rx.Component:
    status_color = rx.match(
        tx["status"],
        ("Completed", "text-green-500"),
        ("Pending", "text-yellow-500"),
        ("Failed", "text-red-500"),
        "text-gray-500",
    )
    return rx.el.div(
        rx.el.div(
            rx.el.strong(tx["type"], class_name="md:hidden pr-2"),
            tx["type"],
            class_name="font-semibold",
        ),
        rx.el.div(tx["amount"], class_name="hidden md:block"),
        rx.el.div(
            tx["date"], class_name="text-gray-500 dark:text-gray-400 hidden md:block"
        ),
        rx.el.div(
            rx.el.strong(tx["status"], class_name="md:hidden pr-2"),
            tx["status"],
            class_name=f"font-medium {status_color}",
        ),
        rx.el.div(tx["hash"], class_name="font-mono text-xs hidden lg:block truncate"),
        class_name="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-4 px-6 py-4 items-center border-b "
        + rx.cond(
            AppState.is_dark_mode,
            "border-gray-700 hover:bg-gray-800/50",
            "border-gray-200 hover:bg-gray-50/50",
        ),
    )


def staking_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            staking_info_card("Staking Tier", WalletState.staking_tier, "tier"),
            staking_info_card("Staked ASRA", WalletState.staked_asra, "asra"),
            staking_info_card(
                "Unrealized Rewards", WalletState.staking_rewards, "asra"
            ),
            staking_info_card("Days Remaining", WalletState.days_remaining, "days"),
            class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6",
        ),
        rx.el.div(
            rx.el.button(
                "Stake",
                on_click=WalletState.open_stake_modal,
                class_name="wallet-button",
            ),
            rx.el.button(
                "Unstake",
                on_click=WalletState.open_unstake_modal,
                class_name="wallet-button",
            ),
            class_name="flex items-center gap-4 mb-8",
        ),
        transaction_history(),
        stake_modal(),
        unstake_modal(),
        class_name="max-w-7xl mx-auto w-full",
    )


def staking_info_card(title: str, value: rx.Var, type: str) -> rx.Component:
    icon_map = {"tier": "award", "asra": "dollar-sign", "days": "clock"}
    return rx.el.div(
        rx.el.div(
            rx.el.p(title, class_name="text-sm text-gray-400"),
            rx.el.div(
                rx.icon(icon_map[type], class_name="h-6 w-6"),
                rx.el.p(value.to_string(), class_name="text-3xl font-bold"),
                class_name="flex items-center gap-3",
            ),
            class_name="flex-1",
        ),
        class_name="flex items-center p-6 rounded-xl shadow-md border "
        + rx.cond(
            AppState.is_dark_mode,
            "bg-gray-800 border-gray-700",
            "bg-white border-gray-200",
        ),
    )


def _transaction_modal(
    title: str, is_open: rx.Var[bool], on_close: rx.event.EventHandler, *children
) -> rx.Component:
    return modal_overlay(
        is_open,
        on_close,
        rx.el.div(
            rx.el.div(
                rx.el.h3(title, class_name="text-lg font-bold"),
                rx.el.button(
                    rx.icon("x"),
                    on_click=on_close,
                    class_name="p-1 rounded-full hover:bg-gray-200 dark:hover:bg-gray-600",
                ),
                class_name="flex justify-between items-center p-4 border-b dark:border-gray-600",
            ),
            rx.el.form(
                *children,
                class_name="p-6 space-y-4",
                on_submit=WalletState.mock_transaction,
                reset_on_submit=True,
            ),
            rx.cond(
                WalletState.transaction_hash != "",
                rx.el.div(
                    rx.el.p("Transaction Hash:", class_name="font-semibold"),
                    rx.el.p(
                        WalletState.transaction_hash,
                        class_name="text-xs font-mono break-all text-gray-500",
                    ),
                    class_name="p-4 bg-gray-100 dark:bg-gray-700/50 rounded-b-xl border-t dark:border-gray-600",
                ),
                None,
            ),
            class_name="w-full max-w-md rounded-xl shadow-2xl bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100",
        ),
    )


def deposit_modal() -> rx.Component:
    return _transaction_modal(
        "Deposit USDT",
        WalletState.is_deposit_modal_open,
        WalletState.close_deposit_modal,
        _form_input("amount", "Amount (USDT)", type="number"),
        rx.el.p(
            "You will be prompted to confirm this transaction in your connected wallet.",
            class_name="text-xs text-gray-500",
        ),
        rx.el.button("Deposit", type="submit", class_name="w-full wallet-button"),
    )


def withdraw_modal() -> rx.Component:
    return _transaction_modal(
        "Withdraw USDT",
        WalletState.is_withdraw_modal_open,
        WalletState.close_withdraw_modal,
        _form_input("amount", "Amount (USDT)", type="number"),
        _form_input("address", "Wallet Address"),
        rx.el.button("Withdraw", type="submit", class_name="w-full wallet-button"),
    )


def swap_modal() -> rx.Component:
    return _transaction_modal(
        "Swap USDT for ASRA",
        WalletState.is_swap_modal_open,
        WalletState.close_swap_modal,
        _form_input("usdt_amount", "Amount (USDT)", type="number"),
        rx.el.p("Est. ASRA Received: 0.00", class_name="text-sm text-gray-500"),
        rx.el.p("Rate: 1 USDT = 45.5 ASRA (mock)", class_name="text-xs text-gray-500"),
        rx.el.button("Swap", type="submit", class_name="w-full wallet-button"),
    )


def stake_modal() -> rx.Component:
    return _transaction_modal(
        "Stake ASRA",
        WalletState.is_stake_modal_open,
        WalletState.close_stake_modal,
        _form_input("amount", "Amount (ASRA)", type="number"),
        rx.el.p(
            "Staking will lock your tokens for a minimum of 90 days.",
            class_name="text-xs text-gray-500",
        ),
        rx.el.button("Stake", type="submit", class_name="w-full wallet-button"),
    )


def unstake_modal() -> rx.Component:
    return _transaction_modal(
        "Unstake ASRA",
        WalletState.is_unstake_modal_open,
        WalletState.close_unstake_modal,
        _form_input("amount", "Amount (ASRA)", type="number"),
        rx.el.p(
            "Unstaking will start a 7-day cooldown period.",
            class_name="text-xs text-gray-500",
        ),
        rx.el.button("Unstake", type="submit", class_name="w-full wallet-button"),
    )


def projects_page() -> rx.Component:
    return rx.el.div(
        rx.el.h1("Projects", class_name="text-3xl font-bold mb-6"),
        rx.el.div(
            rx.foreach(ProjectsState.projects, project_card),
            class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6",
        ),
        dispute_modal(),
        class_name="p-4 md:p-6",
    )


def chat_community_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1("Chat & Community", class_name="text-3xl font-bold"),
            community_toggle(),
            class_name="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-6",
        ),
        rx.match(
            AppState.community_view,
            ("Chat", chat_interface()),
            ("Community", dao_community_view()),
        ),
        class_name="p-4 md:p-6",
    )


def community_toggle() -> rx.Component:
    return rx.el.div(
        rx.el.button(
            "Chat",
            on_click=lambda: AppState.set_community_view("Chat"),
            class_name=rx.cond(
                AppState.community_view == "Chat",
                "px-4 py-2 rounded-l-lg bg-teal-600 text-white font-semibold",
                "px-4 py-2 rounded-l-lg bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600",
            ),
        ),
        rx.el.button(
            "Community",
            on_click=lambda: AppState.set_community_view("Community"),
            class_name=rx.cond(
                AppState.community_view == "Community",
                "px-4 py-2 rounded-r-lg bg-teal-600 text-white font-semibold",
                "px-4 py-2 rounded-r-lg bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600",
            ),
        ),
        class_name="flex",
    )


def chat_interface() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.foreach(ChatState.messages, message_bubble),
                rx.cond(ChatState.is_typing, typing_indicator(), None),
                class_name="flex-1 p-4 space-y-4",
            ),
            id="chat-box",
            class_name="flex flex-col-reverse h-[65vh] overflow-y-auto border rounded-t-xl transition-colors "
            + rx.cond(
                AppState.is_dark_mode,
                "bg-gray-800 border-gray-700",
                "bg-white border-gray-200",
            ),
        ),
        rx.el.form(
            rx.el.input(
                name="message",
                placeholder="Type a message...",
                class_name="flex-1 p-3 rounded-l-lg focus:outline-none transition-colors "
                + rx.cond(
                    AppState.is_dark_mode,
                    "bg-gray-700 placeholder-gray-400",
                    "bg-gray-100 placeholder-gray-500",
                ),
            ),
            rx.el.button(
                rx.icon("send", class_name="h-5 w-5"),
                type="submit",
                class_name="p-3 bg-teal-600 text-white rounded-r-lg hover:bg-teal-700 transition-colors",
            ),
            on_submit=ChatState.send_message,
            reset_on_submit=True,
            class_name="flex border rounded-b-xl shadow-md transition-colors "
            + rx.cond(AppState.is_dark_mode, "border-gray-700", "border-gray-200"),
        ),
        class_name="max-w-4xl mx-auto w-full font-['Lato']",
    )


def message_bubble(message: Message) -> rx.Component:
    is_user = message["sender"] == "You"
    return rx.el.div(
        rx.el.div(
            rx.image(src=message["avatar"], class_name="h-8 w-8 rounded-full"),
            rx.el.div(
                rx.el.div(
                    rx.el.p(message["text"], class_name="text-sm"),
                    class_name="p-3 rounded-xl max-w-md "
                    + rx.cond(
                        is_user,
                        "bg-teal-600 text-white rounded-br-none",
                        "bg-gray-200 dark:bg-gray-700 rounded-bl-none",
                    ),
                ),
                rx.el.p(
                    message["timestamp"],
                    class_name="text-xs text-gray-500 dark:text-gray-400 mt-1",
                ),
                class_name="flex flex-col "
                + rx.cond(is_user, "items-end", "items-start"),
            ),
            class_name="flex items-start gap-3 "
            + rx.cond(is_user, "flex-row-reverse", ""),
        ),
        class_name="flex " + rx.cond(is_user, "justify-end", "justify-start"),
    )


def typing_indicator() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.span(
                class_name="h-2 w-2 bg-gray-400 rounded-full animate-bounce",
                style={"animationDelay": "-0.3s"},
            ),
            rx.el.span(
                class_name="h-2 w-2 bg-gray-400 rounded-full animate-bounce",
                style={"animationDelay": "-0.15s"},
            ),
            rx.el.span(class_name="h-2 w-2 bg-gray-400 rounded-full animate-bounce"),
            class_name="flex items-center gap-1 p-3 bg-gray-200 dark:bg-gray-700 rounded-xl rounded-bl-none",
        ),
        class_name="flex justify-start px-4 py-2",
    )


def dao_community_view() -> rx.Component:
    return rx.el.div(
        rx.el.h2("DAO Governance Proposals", class_name="text-2xl font-bold mb-4"),
        rx.el.div(
            rx.foreach(AppState.proposals, proposal_card),
            class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6",
        ),
        class_name="max-w-7xl mx-auto w-full",
    )


def proposal_card(proposal: Proposal) -> rx.Component:
    progress = proposal["votes"] / proposal["threshold"] * 100
    return rx.el.div(
        rx.el.h3(proposal["title"], class_name="font-semibold text-lg mb-2"),
        rx.el.p(
            proposal["description"],
            class_name="text-sm text-gray-500 dark:text-gray-400 mb-4 h-12",
        ),
        rx.el.div(
            rx.el.div(class_name="flex-1"),
            rx.el.div(
                rx.el.div(
                    style={"width": f"{progress.to_string()}%"},
                    class_name="h-full bg-teal-500 rounded-full transition-all duration-500",
                ),
                class_name="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2",
            ),
            rx.el.p(
                f"{proposal['votes'].to_string()} / {proposal['threshold'].to_string()} ASRA",
                class_name="text-xs text-gray-500 dark:text-gray-400 text-right mt-1",
            ),
            class_name="mb-4",
        ),
        rx.el.div(
            rx.match(
                proposal["status"],
                (
                    "voting",
                    rx.el.button(
                        "Vote",
                        on_click=lambda: AppState.vote_on_proposal(proposal["id"]),
                        class_name="w-full py-2 px-4 bg-teal-600 text-white rounded-lg hover:bg-teal-700 transition-colors font-semibold",
                    ),
                ),
                (
                    "passed",
                    rx.el.button(
                        "Execute",
                        disabled=True,
                        class_name="w-full py-2 px-4 bg-yellow-500 text-white rounded-lg font-semibold opacity-70 cursor-not-allowed",
                    ),
                ),
                (
                    "executed",
                    rx.el.button(
                        "Executed",
                        disabled=True,
                        class_name="w-full py-2 px-4 bg-green-600 text-white rounded-lg font-semibold opacity-70 cursor-not-allowed",
                    ),
                ),
            ),
            class_name="mt-auto",
        ),
        class_name="p-6 rounded-xl shadow-md border flex flex-col transition-colors "
        + rx.cond(
            AppState.is_dark_mode,
            "bg-gray-800 border-gray-700",
            "bg-white border-gray-200",
        ),
    )


def token_metrics_panel() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h2("ASRA Token Metrics", class_name="text-xl font-semibold"),
            rx.el.button(
                "Refresh",
                rx.icon("refresh-cw", class_name="ml-2 h-4 w-4"),
                on_click=AppState.refresh_metrics,
                class_name="flex items-center px-4 py-2 text-sm bg-teal-600 text-white rounded-lg hover:bg-teal-700 transition-colors",
            ),
            class_name="flex justify-between items-center mb-4",
        ),
        rx.el.div(
            metric_card("Total Supply", AppState.token_metrics["total_supply"]),
            metric_card(
                "Circulating Supply", AppState.token_metrics["circulating_supply"]
            ),
            metric_card("Total Staked", AppState.token_metrics["total_staked"]),
            metric_card("Total Unstaking", AppState.token_metrics["total_unstaking"]),
            metric_card("Total Burned", AppState.token_metrics["total_burned"]),
            class_name="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4 mb-6",
        ),
        rx.el.div(
            rx.recharts.line_chart(
                rx.recharts.cartesian_grid(stroke_dasharray="3 3", stroke_opacity=0.2),
                rx.recharts.x_axis(
                    data_key="name",
                    stroke=rx.cond(AppState.is_dark_mode, "#6B7280", "#9CA3AF"),
                ),
                rx.recharts.y_axis(
                    stroke=rx.cond(AppState.is_dark_mode, "#6B7280", "#9CA3AF")
                ),
                rx.recharts.tooltip(
                    content_style={
                        "backgroundColor": rx.cond(
                            AppState.is_dark_mode, "#1F2937", "#FFFFFF"
                        ),
                        "borderColor": "#374151",
                    }
                ),
                rx.recharts.line(
                    type="monotone",
                    data_key="price",
                    stroke="#2DD4BF",
                    active_dot={"r": 8},
                ),
                data=AppState.price_chart_data,
                height=250,
            ),
            class_name="w-full",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(class_name="w-3 h-3 rounded-full bg-[#2DD4BF]"),
                rx.el.p("Price", class_name="text-sm"),
                class_name="flex items-center gap-2",
            ),
            class_name="flex justify-center mt-2",
        ),
        class_name="p-6 rounded-xl shadow-md border transition-colors "
        + rx.cond(
            AppState.is_dark_mode,
            "bg-gray-800 border-gray-700",
            "bg-white border-gray-200",
        ),
    )


def metric_card(title: str, value: rx.Var[int]) -> rx.Component:
    return rx.el.div(
        rx.el.p(title, class_name="text-sm text-gray-400"),
        rx.el.p(value.to_string(), class_name="text-2xl font-bold"),
        class_name="p-4 rounded-lg "
        + rx.cond(AppState.is_dark_mode, "bg-gray-700/50", "bg-gray-50"),
    )


def form_panel() -> rx.Component:
    return rx.el.div(upload_skill_form(), create_project_form(), class_name="space-y-6")


def _form_wrapper(title: str, *children) -> rx.Component:
    return rx.el.div(
        rx.el.h3(title, class_name="text-lg font-semibold mb-4"),
        rx.el.form(
            *children,
            rx.el.button(
                "Submit",
                type="submit",
                class_name="w-full mt-4 px-4 py-2 bg-teal-600 text-white rounded-lg hover:bg-teal-700 transition-colors font-semibold",
            ),
            on_submit=AppState.handle_form_submit,
            reset_on_submit=True,
            class_name="space-y-4",
        ),
        class_name="p-6 rounded-xl shadow-md border transition-colors "
        + rx.cond(
            AppState.is_dark_mode,
            "bg-gray-800 border-gray-700",
            "bg-white border-gray-200",
        ),
    )


def _form_input(name: str, placeholder: str, type: str = "text") -> rx.Component:
    base_class = "w-full p-2 border rounded-md transition-colors text-sm "
    dark_class = "bg-gray-700 border-gray-600 placeholder-gray-400 focus:ring-teal-500 focus:border-teal-500"
    light_class = "bg-white border-gray-300 placeholder-gray-500 focus:ring-teal-500 focus:border-teal-500"
    return rx.el.input(
        name=name,
        placeholder=placeholder,
        type=type,
        class_name=base_class + rx.cond(AppState.is_dark_mode, dark_class, light_class),
        required=True,
    )


def upload_skill_form() -> rx.Component:
    return _form_wrapper(
        "Upload Skill",
        _form_input("skill_name", "Skill Name (e.g., Solidity)"),
        _form_input("category", "Category (e.g., Smart Contracts)"),
        _form_input("description", "Description"),
        _form_input("rate_per_hour", "Rate per Hour ($)", type="number"),
    )


def create_project_form() -> rx.Component:
    return _form_wrapper(
        "Create Project",
        _form_input("project_title", "Project Title (e.g., NFT Marketplace)"),
        _form_input("project_category", "Category (e.g., DeFi)"),
        _form_input("budget", "Budget ($)", type="number"),
        _form_input("reward_asra", "Reward (ASRA)", type="number"),
    )


def suggestion_feed() -> rx.Component:
    return rx.el.div(
        rx.el.h3("Suggestion Feed", class_name="text-lg font-semibold mb-4"),
        rx.el.div(
            rx.foreach(AppState.suggestions, suggestion_card),
            class_name="grid grid-cols-1 md:grid-cols-2 gap-4",
        ),
        class_name="p-6 rounded-xl shadow-md border h-full transition-colors "
        + rx.cond(
            AppState.is_dark_mode,
            "bg-gray-800 border-gray-700",
            "bg-white border-gray-200",
        ),
    )


def suggestion_card(suggestion: Suggestion) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.image(src=suggestion["avatar"], class_name="h-12 w-12 rounded-full"),
            rx.el.div(
                rx.el.p(suggestion["name"], class_name="font-semibold"),
                rx.el.p(suggestion["title"], class_name="text-sm text-gray-400"),
                class_name="flex-1",
            ),
            class_name="flex items-center gap-3 mb-3",
        ),
        rx.el.div(
            rx.foreach(
                suggestion["tags"],
                lambda tag: rx.el.span(
                    tag,
                    class_name="text-xs px-2 py-1 rounded-full "
                    + rx.cond(AppState.is_dark_mode, "bg-gray-600", "bg-gray-200"),
                ),
            ),
            class_name="flex flex-wrap gap-2 mb-4",
        ),
        rx.el.div(
            rx.el.button(
                "Chat",
                on_click=AppState.open_chat_modal,
                class_name="flex-1 text-sm py-2 px-4 rounded-md border transition-colors "
                + rx.cond(
                    AppState.is_dark_mode,
                    "bg-gray-700 border-gray-600 hover:bg-gray-600",
                    "bg-white border-gray-300 hover:bg-gray-100",
                ),
            ),
            rx.el.button(
                "View Profile",
                on_click=lambda: AppState.open_profile_modal(suggestion),
                class_name="flex-1 text-sm py-2 px-4 rounded-md text-white transition-colors bg-teal-600 hover:bg-teal-700",
            ),
            class_name="flex gap-2",
        ),
        class_name="p-4 rounded-lg border transition-colors "
        + rx.cond(
            AppState.is_dark_mode,
            "bg-gray-700/50 border-gray-600/50 hover:border-gray-500",
            "bg-white border-gray-200 hover:border-gray-300",
        ),
    )


def modal_overlay(
    is_open: rx.Var[bool], on_close: rx.event.EventHandler, *children
) -> rx.Component:
    return rx.cond(
        is_open,
        rx.el.div(
            rx.el.div(on_click=on_close, class_name="fixed inset-0 bg-black/60 z-50"),
            rx.el.div(
                *children,
                class_name="fixed inset-0 z-50 flex items-center justify-center p-4",
            ),
            class_name="font-['Lato']",
        ),
        None,
    )


def chat_modal() -> rx.Component:
    return modal_overlay(
        AppState.is_chat_modal_open,
        AppState.close_chat_modal,
        rx.el.div(
            rx.el.div(
                rx.el.h3("Chat", class_name="text-lg font-bold"),
                rx.el.button(
                    rx.icon("x"),
                    on_click=AppState.close_chat_modal,
                    class_name="p-1 rounded-full hover:bg-gray-200 dark:hover:bg-gray-600",
                ),
                class_name="flex justify-between items-center p-4 border-b dark:border-gray-600",
            ),
            rx.el.div("Chat interface coming soon...", class_name="p-6 text-center"),
            class_name="w-full max-w-lg rounded-xl shadow-2xl bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100",
        ),
    )


def project_card(project: Project) -> rx.Component:
    status_colors = {
        "Pending Confirmation": "bg-yellow-500",
        "In Progress": "bg-blue-500",
        "Completed": "bg-green-600",
        "Disputed": "bg-red-600",
    }
    return rx.el.div(
        rx.el.div(
            rx.el.h3(project["title"], class_name="font-semibold text-lg truncate"),
            rx.el.div(
                rx.el.div(
                    class_name=f"h-2 w-2 rounded-full {status_colors.get(project['status'])}"
                ),
                rx.el.p(project["status"], class_name="text-xs"),
                class_name="flex items-center gap-2 px-2 py-1 rounded-full text-xs font-medium "
                + rx.cond(
                    AppState.is_dark_mode,
                    "bg-gray-700 text-gray-300",
                    "bg-gray-100 text-gray-600",
                ),
            ),
            class_name="flex justify-between items-center mb-3",
        ),
        rx.el.div(
            rx.el.p("Budget: ", class_name="text-sm text-gray-400"),
            rx.el.p(f"${project['budget'].to_string()}", class_name="font-semibold"),
            class_name="flex items-baseline gap-1",
        ),
        rx.el.div(
            rx.el.p("Reward: ", class_name="text-sm text-gray-400"),
            rx.el.p(
                f"{project['reward'].to_string()} ASRA", class_name="font-semibold"
            ),
            class_name="flex items-baseline gap-1 mb-4",
        ),
        rx.el.div(
            rx.el.p("Client: ", class_name="text-xs text-gray-500"),
            rx.el.p(project["client"], class_name="text-xs font-mono truncate"),
            class_name="flex items-center gap-2",
        ),
        rx.el.div(
            rx.el.p("Worker: ", class_name="text-xs text-gray-500"),
            rx.el.p(project["worker"], class_name="text-xs font-mono truncate"),
            class_name="flex items-center gap-2 mb-4",
        ),
        rx.el.div(
            rx.el.button(
                "Confirm Work",
                on_click=lambda: ProjectsState.confirm_work(project["id"]),
                class_name="project-action-button bg-green-600 hover:bg-green-700",
            ),
            rx.el.button(
                "Request Revision",
                on_click=lambda: ProjectsState.request_revision(project["id"]),
                class_name="project-action-button bg-yellow-500 hover:bg-yellow-600",
            ),
            rx.el.button(
                "Submit Work",
                on_click=lambda: ProjectsState.submit_work(project["id"]),
                class_name="project-action-button bg-blue-600 hover:bg-blue-700",
            ),
            rx.el.button(
                "Open Dispute",
                on_click=lambda: ProjectsState.open_dispute_modal(project["id"]),
                class_name="project-action-button bg-red-600 hover:bg-red-700 col-span-2 md:col-span-1",
            ),
            class_name="grid grid-cols-2 md:grid-cols-2 gap-2 mt-auto",
        ),
        class_name="p-5 rounded-xl shadow-md border flex flex-col transition-colors "
        + rx.cond(
            AppState.is_dark_mode,
            "bg-gray-800 border-gray-700",
            "bg-white border-gray-200",
        ),
    )


def dispute_modal() -> rx.Component:
    return modal_overlay(
        ProjectsState.is_dispute_modal_open,
        ProjectsState.close_dispute_modal,
        rx.el.div(
            rx.el.div(
                rx.el.h3("Open a Dispute", class_name="text-lg font-bold"),
                rx.el.button(
                    rx.icon("x"),
                    on_click=ProjectsState.close_dispute_modal,
                    class_name="p-1 rounded-full hover:bg-gray-200 dark:hover:bg-gray-600",
                ),
                class_name="flex justify-between items-center p-4 border-b dark:border-gray-600",
            ),
            rx.el.form(
                _form_input("reason", "Reason for dispute"),
                _form_input("proof", "Link to proof (optional)"),
                rx.el.div(
                    rx.el.label("Dispute Fee", class_name="text-sm font-medium"),
                    rx.el.select(
                        rx.el.option("50 ASRA (Standard)", value="asra"),
                        rx.el.option("10% of Budget", value="percentage"),
                        name="fee_type",
                        class_name="w-full p-2 border rounded-md transition-colors text-sm "
                        + rx.cond(
                            AppState.is_dark_mode,
                            "bg-gray-700 border-gray-600",
                            "bg-white border-gray-300",
                        ),
                    ),
                    class_name="space-y-2",
                ),
                rx.el.button(
                    "Submit Dispute",
                    type="submit",
                    class_name="w-full wallet-button bg-red-600 hover:bg-red-700",
                ),
                on_submit=ProjectsState.submit_dispute,
                reset_on_submit=True,
                class_name="p-6 space-y-4",
            ),
            class_name="w-full max-w-md rounded-xl shadow-2xl bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100",
        ),
    )


def profile_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1("Profile", class_name="text-3xl font-bold"),
            profile_toggle(),
            class_name="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-6",
        ),
        rx.match(
            ProfileState.profile_view,
            ("Worker", worker_profile_view()),
            ("Client", client_profile_view()),
        ),
        class_name="p-4 md:p-6",
    )


def profile_toggle() -> rx.Component:
    return rx.el.div(
        rx.el.button(
            "Worker",
            on_click=lambda: ProfileState.set_profile_view("Worker"),
            class_name=rx.cond(
                ProfileState.profile_view == "Worker",
                "px-4 py-2 rounded-l-lg bg-teal-600 text-white font-semibold",
                "px-4 py-2 rounded-l-lg bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600",
            ),
        ),
        rx.el.button(
            "Client",
            on_click=lambda: ProfileState.set_profile_view("Client"),
            class_name=rx.cond(
                ProfileState.profile_view == "Client",
                "px-4 py-2 rounded-r-lg bg-teal-600 text-white font-semibold",
                "px-4 py-2 rounded-r-lg bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600",
            ),
        ),
        class_name="flex",
    )


def worker_profile_view() -> rx.Component:
    return rx.el.div(
        profile_header("Worker"),
        rx.el.div(
            _profile_section(
                "Portfolio",
                "portfolio",
                rx.el.div(
                    rx.foreach(ProfileState.portfolio_items, portfolio_item_card),
                    class_name="grid grid-cols-1 md:grid-cols-2 gap-4",
                ),
            ),
            _profile_section(
                "Job History",
                "job_history",
                rx.el.p("Job history details coming soon..."),
            ),
            _profile_section(
                "Transaction History", "tx_history", transaction_history()
            ),
            class_name="space-y-6",
        ),
        class_name="max-w-7xl mx-auto w-full",
    )


def client_profile_view() -> rx.Component:
    return rx.el.div(
        profile_header("Client"),
        rx.el.div(
            _profile_section(
                "Posted Projects",
                "posted_projects",
                rx.el.p("Posted projects details coming soon..."),
            ),
            _profile_section(
                "Transaction History", "tx_history", transaction_history()
            ),
            class_name="space-y-6",
        ),
        class_name="max-w-7xl mx-auto w-full",
    )


def profile_header(profile_type: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.image(
                src="https://api.dicebear.com/9.x/initials/svg?seed=User",
                class_name="h-24 w-24 rounded-full border-4 "
                + rx.cond(AppState.is_dark_mode, "border-gray-700", "border-gray-200"),
            ),
            rx.el.div(
                rx.el.h2("Your Profile", class_name="text-2xl font-bold"),
                rx.el.div(
                    rx.el.span("Staking Tier:"),
                    rx.el.span(
                        WalletState.staking_tier,
                        class_name="font-semibold px-2 py-1 text-sm rounded-full bg-teal-100 text-teal-800 dark:bg-teal-900 dark:text-teal-200",
                    ),
                    class_name="flex items-center gap-2 text-gray-500 dark:text-gray-400 mt-1",
                ),
            ),
            class_name="flex items-center gap-6",
        ),
        rx.cond(
            profile_type == "Worker",
            rx.el.div(
                profile_stat_card("Rating", ProfileState.worker_rating, "star"),
                profile_stat_card("Rank", ProfileState.worker_rank, "bar-chart-2"),
                profile_stat_card(
                    "Completed Jobs", ProfileState.completed_jobs, "check_check"
                ),
                class_name="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6",
            ),
            rx.el.div(
                profile_stat_card(
                    "Projects Posted", ProfileState.client_projects_posted, "briefcase"
                ),
                profile_stat_card(
                    "Total Spending",
                    ProfileState.client_total_spending,
                    "dollar-sign",
                    prefix="$",
                ),
                profile_stat_card("DAO Votes", ProfileState.client_dao_votes, "gavel"),
                class_name="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6",
            ),
        ),
        class_name="p-6 rounded-xl shadow-md border mb-6 "
        + rx.cond(
            AppState.is_dark_mode,
            "bg-gray-800 border-gray-700",
            "bg-white border-gray-200",
        ),
    )


def profile_stat_card(
    title: str, value: rx.Var, icon: str, prefix: str = ""
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name="h-5 w-5 text-gray-400"),
            rx.el.p(title, class_name="text-sm text-gray-400"),
            class_name="flex items-center gap-2",
        ),
        rx.el.p(f"{prefix}{value.to_string()}", class_name="text-2xl font-bold"),
        class_name="p-4 rounded-lg "
        + rx.cond(AppState.is_dark_mode, "bg-gray-700/50", "bg-gray-50"),
    )


def _profile_section(
    title: str, section_key: str, content: rx.Component
) -> rx.Component:
    is_expanded = ProfileState.expanded_sections[section_key]
    return rx.el.div(
        rx.el.button(
            rx.el.h3(title, class_name="text-lg font-semibold"),
            rx.icon(
                rx.cond(is_expanded, "chevron-down", "chevron-right"),
                class_name="transition-transform",
            ),
            on_click=lambda: ProfileState.toggle_section(section_key),
            class_name="flex justify-between items-center w-full p-4 cursor-pointer",
        ),
        rx.cond(
            is_expanded,
            rx.el.div(content, class_name="p-4 border-t dark:border-gray-700"),
            None,
        ),
        class_name="rounded-xl shadow-md border "
        + rx.cond(
            AppState.is_dark_mode,
            "bg-gray-800 border-gray-700",
            "bg-white border-gray-200",
        ),
    )


def portfolio_item_card(item: dict) -> rx.Component:
    return rx.el.div(
        rx.image(
            src=item["image_url"], class_name="w-full h-32 object-cover rounded-t-lg"
        ),
        rx.el.div(
            rx.el.h4(item["title"], class_name="font-semibold"),
            rx.el.p(item["description"], class_name="text-xs text-gray-500"),
            class_name="p-3",
        ),
        class_name="rounded-lg border dark:border-gray-700 overflow-hidden",
    )


def profile_modal() -> rx.Component:
    return modal_overlay(
        AppState.is_profile_modal_open,
        AppState.close_profile_modal,
        rx.cond(
            AppState.selected_profile,
            rx.el.div(
                rx.el.button(
                    rx.icon("x"),
                    on_click=AppState.close_profile_modal,
                    class_name="absolute top-4 right-4 p-1 rounded-full hover:bg-gray-200 dark:hover:bg-gray-600",
                ),
                rx.el.div(
                    rx.image(
                        src=AppState.selected_profile["avatar"],
                        class_name="h-24 w-24 rounded-full border-4 border-teal-500",
                    ),
                    rx.el.h2(
                        AppState.selected_profile["name"],
                        class_name="text-2xl font-bold mt-4",
                    ),
                    rx.el.div(
                        rx.el.span("Staking Tier:"),
                        rx.el.span(
                            AppState.selected_profile["staking_level"],
                            class_name="font-semibold px-2 py-1 text-sm rounded-full bg-teal-100 text-teal-800 dark:bg-teal-900 dark:text-teal-200",
                        ),
                        class_name="flex items-center gap-2 text-gray-500 dark:text-gray-400 mt-2",
                    ),
                    class_name="flex flex-col items-center",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.h4("Portfolio", class_name="font-semibold mb-1"),
                        rx.el.a(
                            AppState.selected_profile["portfolio"],
                            href=AppState.selected_profile["portfolio"],
                            is_external=True,
                            class_name="text-teal-500 hover:underline break-all",
                        ),
                        class_name="space-y-1",
                    ),
                    rx.el.div(
                        rx.el.h4("User Hash", class_name="font-semibold mb-1"),
                        rx.el.p(
                            AppState.selected_profile["hash"],
                            class_name="text-xs text-gray-500 break-all",
                        ),
                        class_name="space-y-1",
                    ),
                    class_name="p-6 space-y-4",
                ),
                class_name="w-full max-w-md rounded-xl shadow-2xl overflow-hidden bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100",
            ),
            rx.el.div(),
        ),
    )
import reflex as rx
from app.components import header, main_content
from app.state import AppState
from app.states.chat_state import ChatState
from app.states.wallet_state import WalletState
from app.states.projects_state import ProjectsState
from app.states.profile_state import ProfileState


def index() -> rx.Component:
    """The main view of the app."""
    return rx.el.div(
        header(),
        main_content(),
        class_name=rx.cond(AppState.is_dark_mode, "dark bg-gray-900", "bg-white"),
    )


app = rx.App(
    theme=rx.theme(appearance="light", accent_color="teal"),
    stylesheets=["/css/styles.css"],
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Lato:wght@400;700&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(
    index, on_load=[AppState.on_load, ProjectsState.on_load, ProfileState.on_load]
)
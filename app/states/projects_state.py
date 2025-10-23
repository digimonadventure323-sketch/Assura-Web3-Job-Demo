import reflex as rx
from typing import TypedDict, Literal
import random

ProjectStatus = Literal["Pending Confirmation", "In Progress", "Completed", "Disputed"]


class Project(TypedDict):
    id: int
    title: str
    budget: int
    reward: int
    status: ProjectStatus
    client: str
    worker: str


class ProjectsState(rx.State):
    projects: list[Project] = []
    is_dispute_modal_open: bool = False
    dispute_project_id: int | None = None

    @rx.event
    def on_load(self):
        if not self.projects:
            self._initialize_projects()

    def _initialize_projects(self):
        statuses: list[ProjectStatus] = [
            "Pending Confirmation",
            "In Progress",
            "Completed",
            "Disputed",
        ]
        titles = [
            "DeFi Lending Protocol",
            "NFT Art Marketplace",
            "DAO Voting System",
            "Web3 Gaming Platform",
            "Multi-sig Wallet UI",
            "Token Bridge Audit",
        ]
        for i in range(6):
            self.projects.append(
                {
                    "id": 201 + i,
                    "title": titles[i],
                    "budget": random.randint(5000, 20000),
                    "reward": random.randint(100, 1000),
                    "status": random.choice(statuses),
                    "client": f"0x...{random.randbytes(4).hex()}",
                    "worker": f"0x...{random.randbytes(4).hex()}",
                }
            )

    @rx.event
    def confirm_work(self, project_id: int):
        for i, p in enumerate(self.projects):
            if p["id"] == project_id:
                self.projects[i]["status"] = "Completed"
                break
        yield rx.toast(
            "Work Confirmed",
            description=f"Project #{project_id} marked as complete.",
            duration=3000,
        )

    @rx.event
    def request_revision(self, project_id: int):
        yield rx.toast(
            "Revision Requested",
            description=f"Worker notified for project #{project_id}.",
            duration=3000,
        )

    @rx.event
    def submit_work(self, project_id: int):
        yield rx.toast(
            "Work Submitted",
            description=f"Client has been notified to review your work for project #{project_id}.",
            duration=3000,
        )

    @rx.event
    def open_dispute_modal(self, project_id: int):
        self.dispute_project_id = project_id
        self.is_dispute_modal_open = True

    @rx.event
    def close_dispute_modal(self):
        self.is_dispute_modal_open = False
        self.dispute_project_id = None

    @rx.event
    def submit_dispute(self, form_data: dict):
        project_id = self.dispute_project_id
        for i, p in enumerate(self.projects):
            if p["id"] == project_id:
                self.projects[i]["status"] = "Disputed"
                break
        self.is_dispute_modal_open = False
        self.dispute_project_id = None
        yield rx.toast(
            "Dispute Opened",
            description=f"A DAO proposal has been created for project #{project_id}.",
            duration=4000,
        )
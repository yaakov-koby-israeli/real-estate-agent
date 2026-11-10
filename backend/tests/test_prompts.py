from app.agent.prompts import build_system_prompt
from app.models.enums import ProjectCategory
from app.services.chat_flow import FINISH_OPTION


def test_prompt_points_to_the_real_finish_button():
    # The agent tells customers to click this button to reach sales - it must match the real label.
    assert f'"{FINISH_OPTION}"' in build_system_prompt(ProjectCategory.RESIDENTIAL)

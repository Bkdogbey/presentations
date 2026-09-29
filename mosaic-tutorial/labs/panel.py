"""An info panel that hides how many victims are left.

Save this file as src/experiment/panel.py, then in main.py:

    from .panel import NoProgressPanel

    gui = SAREnvGUI(env, config=config, llm_client=llm_client,
                    info_panel=NoProgressPanel(800, 400, 400))

The three numbers are the panel's position and size in the 800-px window:
x offset (the game view's width), panel width, and panel height.
"""
from mosaic.gui.info import InfoPanel


class NoProgressPanel(InfoPanel):
    """The stock info panel without the "Remaining" victim count."""

    def _mission_html(self, rescued=0, remaining=0, steps=0, max_steps=0,
                      inv_text="None", inv_color="#FFFFFF"):
        return (
            f"<font pixel_size='{self._body_size}'>"
            f"Rescued: <font color='#32CD32'>{rescued}</font><br>"
            f"Steps: {steps}/{max_steps}"
            f"&nbsp;|&nbsp;"
            f"Inventory: <font color='{inv_color}'>{inv_text}</font>"
            f"</font><hr>"
        )

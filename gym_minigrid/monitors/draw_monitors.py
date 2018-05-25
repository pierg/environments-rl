from properties.avoid import *
from monitors.patterns.precedence import *
from monitors.patterns.absence import *
from monitors.patterns.universality import *
from configurations import config_grabber as cg


def on_monitoring(name, state, **kwargs):
    """
    Notify for violations
    :param type: Can be of state/observations mismatch or violation of safety property
    :param unsafe_actions: list of unsafe actions (in case of violation type)
    :return:
    """

    if state == "mismatch":
        logging.warning(name + " mismatch!!!!")

    if state == "monitoring":
        logging.info(name + " monitoring")

    if state == "shaping":
        if kwargs:
            logging.info(name + " shaping")
            logging.info("     shaped_reward = " + str(shaped_reward))
        else:
            logging.warning("%s ERROR. missing action and reward", name)

    if state == "violation":
        if kwargs:
            logging.warning("%s violation blocked", name)
            logging.info("shaped_reward=" + str(kwargs.get("shaped_reward")) + " unsafe_action=" + str(kwargs.get("unsafe_action")))
        else:
            logging.warning("%s ERROR. missing action and reward", name)



class PrintMonitors:
    if __name__ == "__main__":
        config = cg.Configuration.grab("test")


        for avoid_obj in config.monitors.properties.avoid:
            monitor = Avoid("absence_" + avoid_obj.name, avoid_obj.name, on_monitoring, avoid_obj.rewards)
            monitor.draw()

        for precedence_obj in config.monitors.patterns.precedence:
            monitor = Precedence("precedence_" + precedence_obj.name, precedence_obj.conditions, on_monitoring, precedence_obj.rewards)
            monitor.draw()

        for universality_obj in config.monitors.patterns.universality:
            monitor = Universality("universality_" + universality_obj.name, universality_obj, on_monitoring, universality_obj.rewards)
            monitor.draw()

        for absence_obj in config.monitors.patterns.absence:
            monitor = Absence("absence_" + absence_obj.name, absence_obj, on_monitoring, absence_obj.rewards)
            monitor.draw()
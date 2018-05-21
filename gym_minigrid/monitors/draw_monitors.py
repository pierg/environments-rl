from monitors.patterns.absence import *
from monitors.patterns.precedence import *
from configurations import config_grabber as cg


def on_monitoring(name, state, **kwargs):
    """
    Notify for violations
    :param type: Can be of state/observations mismatch or violation of safety property
    :param unsafe_actions: list of unsafe actions (in case of violation type)
    :return:
    """

    #if state == "mismatch":
    #    logging.warning(name + " mismatch!!!!")

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
            #logging.warning("%s violation blocked", name)
            logging.info("shaped_reward=" + str(shaped_reward) + " unsafe_action=" + str(unsafe_action))
        else:
            logging.warning("%s ERROR. missing action and reward", name)



class PrintMonitors:
    if __name__ == "__main__":
        # Grab configuration
        config = cg.Configuration.grab()
        for avoid_obj in config.monitors.absence.monitored:
            new_absence_monitor = Absence("absence_" + avoid_obj.name, avoid_obj.name, on_monitoring,avoid_obj.reward)
            new_absence_monitor.draw()

        for precedence_obj in config.monitors.precedence.monitored:
            new_precedence_monitor = Precedence("precedence_" + precedence_obj.name, precedence_obj, on_monitoring, precedence_obj.reward)
            new_precedence_monitor.draw()

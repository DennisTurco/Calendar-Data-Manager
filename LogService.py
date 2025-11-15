import logging
import os
from typing import Optional
from ConfigKeys import ConfigKeys

class LogService:
    _is_configured = False

    @classmethod
    def get_logger(cls, name: Optional[str] = None):
        if not cls._is_configured:
            cls._configure()
        return logging.getLogger(name)

    @classmethod
    def _configure(cls):

        ConfigKeys.load_values_from_json()
        config_dir = ConfigKeys.Keys.CONFIG_DIR.value
        log_file = ConfigKeys.Keys.LOG_FILE.value
        log_level = ConfigKeys.Keys.LOG_SERVICE_LEVEL.value
        max_lines = ConfigKeys.Keys.LOG_SERVICE_MAXLINES.value
        lines_to_keep = ConfigKeys.Keys.LOG_SERVICE_LINESTOKEEP.value

        full_path = os.path.join(config_dir, log_file)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        print(f"[LogService] Writing logs to: {full_path}")

        # -----------------------------------------------
        #   ROTATION BASED ON NUMBER OF LINES (CUSTOM)
        # -----------------------------------------------
        if os.path.exists(full_path):
            with open(full_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            if len(lines) > max_lines:
                print(f"[LogService] Log exceeded {max_lines} lines → clearing and keeping last {lines_to_keep}")

                # Keep only the last N lines
                trimmed = lines[-lines_to_keep:]

                with open(full_path, "w", encoding="utf-8") as f:
                    f.writelines(trimmed)

        # ------------------------------------------------
        #  LOGGER CONFIGURATION
        # ------------------------------------------------
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.getLevelName(log_level.upper()))

        formatter = logging.Formatter(
            "%(asctime)s - [%(levelname)s] (%(filename)s:%(lineno)d) - %(message)s"
        )

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        # File handler
        file_handler = logging.FileHandler(full_path, encoding="utf-8")
        file_handler.setFormatter(formatter)

        root_logger.addHandler(console_handler)
        root_logger.addHandler(file_handler)

        cls._is_configured = True

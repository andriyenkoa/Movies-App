import os
import logging
from config import project_abs_path

logging.basicConfig(
    filename=os.path.join(project_abs_path, 'etl_log.log'),
    encoding="utf-8",
    filemode="a",
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
)

logger = logging.getLogger(__name__)

__all__ = ['logger']

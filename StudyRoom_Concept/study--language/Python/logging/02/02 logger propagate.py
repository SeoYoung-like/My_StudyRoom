import logging

# Root Logger에만 핸들러 설정
logging.basicConfig(level=logging.DEBUG, format="%(name)s - %(message)s")

# 여러 depth의 로거들
logA = logging.getLogger("myproject")
logB = logging.getLogger("myproject.api")
logC = logging.getLogger("myproject.api.views")

logA.info("A에서 찍음")
logB.info("B에서 찍음")
logC.info("C에서 찍음")
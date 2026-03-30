import logging

# ── 설정 ──────────────────────────────────────────
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d — %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename="stage1_practice.log",
    encoding="utf-8",
    filemode="w",
)


# ── 실습: 쇼핑몰 주문 처리 시뮬레이션 ──────────────
def check_stock(item_id: int, quantity: int) -> bool:
    logging.debug("재고 확인 시작: item_id=%d, quantity=%d", item_id, quantity)
    stock = 5  # 실제론 DB 조회
    if quantity > stock:
        logging.warning("재고 부족: 요청=%d, 재고=%d", quantity, stock)
        return False
    logging.info("재고 확인 완료: 충분함")
    return True

def process_payment(amount: int) -> bool:
    logging.debug("결제 시도: amount=%d", amount)
    if amount <= 0:
        logging.error("유효하지 않은 결제 금액: %d", amount)
        return False
    logging.info("결제 성공: %d원", amount)
    return True

def process_order(item_id: int, quantity: int, amount: int):
    logging.info("=== 주문 처리 시작 ===")
    
    if not check_stock(item_id, quantity):
        logging.error("주문 실패: 재고 부족")
        return
    
    if not process_payment(amount):
        logging.critical("결제 시스템 오류 — 즉시 확인 필요")
        return
    
    logging.info("주문 완료: item_id=%d, 수량=%d, 금액=%d원",
                item_id, quantity, amount)

# ── 실행 ──────────────────────────────────────────
process_order(item_id=101, quantity=3, amount=15000)   # 정상
process_order(item_id=102, quantity=10, amount=50000)  # 재고 부족
process_order(item_id=103, quantity=1, amount=-1000)   # 결제 오류
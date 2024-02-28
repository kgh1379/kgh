# 알림 발송 함수 예시
def send_notification(message, recipient):
    # 이메일이나 메신저 API를 사용하여 알림을 발송하는 코드
    # 여기서는 예시로만 기능을 제공하며, 실제 구현은 사용하는 알림 서비스에 맞게 조정해야 함
    print(f"Sending notification to {recipient}: {message}")

# 재고 수량이 적어질 때 알림 발송
def notify_low_stock(item_name, current_quantity, alert_quantity, recipient):
    if current_quantity <= alert_quantity:
        message = f"Warning: Low stock for {item_name}. Current quantity is {current_quantity}."
        send_notification(message, recipient)

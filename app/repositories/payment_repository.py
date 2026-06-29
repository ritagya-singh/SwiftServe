from sqlalchemy.orm import Session

from app.models.payment import Payment


class PaymentRepository:

    def create(
        self,
        db: Session,
        payment: Payment
    ) -> Payment:

        db.add(payment)

        db.commit()

        db.refresh(payment)

        return payment

    def get_by_id(
        self,
        db: Session,
        payment_id: int
    ) -> Payment | None:

        return (

            db.query(Payment)

            .filter(

                Payment.id == payment_id

            )

            .first()

        )

    def get_by_order(
        self,
        db: Session,
        order_id: int
    ) -> Payment | None:

        return (

            db.query(Payment)

            .filter(

                Payment.order_id == order_id

            )

            .first()

        )

    def get_customer_payments(
        self,
        db: Session,
        customer_id: int
    ):

        return (

            db.query(Payment)

            .filter(

                Payment.customer_id == customer_id

            )

            .order_by(

                Payment.created_at.desc()

            )

            .all()

        )

    def update(
        self,
        db: Session,
        payment: Payment
    ) -> Payment:

        db.commit()

        db.refresh(payment)

        return payment

    def delete(
        self,
        db: Session,
        payment: Payment
    ):

        db.delete(payment)

        db.commit()
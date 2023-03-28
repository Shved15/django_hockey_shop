from http import HTTPStatus

import stripe
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from common.views import CommonMixin
from orders.forms import OrderForm
from orders.models import Order
from products.models import Bag

stripe.api_key = settings.STRIPE_SECRET_KEY


class SuccessTemplateView(CommonMixin, TemplateView):
    template_name = 'orders/successfully.html'
    title = 'Shop - Thanks for your order!'


class CanceledTemplateView(TemplateView):
    template_name = 'orders/canceled.html'


class OrderListView(CommonMixin, ListView):
    template_name = 'orders/orders.html'
    title = 'Store - Orders'
    queryset = Order.objects.all()
    ordering = ('-created',)

    # method to display registered user's orders and not all databases
    def get_queryset(self):
        queryset = super(OrderListView, self).get_queryset()
        return queryset.filter(creator=self.request.user)


class OrderDetailView(DetailView):
    template_name = 'orders/order.html'
    model = Order

    def get_context_data(self, **kwargs):
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        # we cannot inherit from the CommonMixin because we need the actual order number
        context['title'] = f'Store - Order №{self.object.id}'
        return context


class OrderCreateView(CommonMixin, CreateView):
    template_name = 'orders/order_create.html'
    form_class = OrderForm
    success_url = reverse_lazy('orders:order_create')
    title = 'Shop - Ordering'

    # it works to create an object, accept all the data, validate the form, etc.
    def post(self, request, *args, **kwargs):
        # make it so that the logic that creates the order object is executed
        super(OrderCreateView, self).post(request, *args, **kwargs)
        bags = Bag.objects.filter(user=self.request.user)
        # stripe logic
        checkout_session = stripe.checkout.Session.create(
            # what is formed from our order
            line_items=bags.stripe_products(),
            metadata={'order_id': self.object.id},
            mode='payment',
            success_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:order_success')),
            cancel_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders:order_cancel')),
        )
        return HttpResponseRedirect(checkout_session.url, status=HTTPStatus.SEE_OTHER)

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super(OrderCreateView, self).form_valid(form)


# from srtipe docs
@csrf_exempt
def stripe_webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        # Fulfill the purchase...
        fulfill_order(session)

        # Passed signature verification
    return HttpResponse(status=200)

    return HttpResponse(status=200)


def fulfill_order(session):
    order_id = int(session.metadata.order_id)
    order = Order.objects.get(id=order_id)
    order.update_after_payment()

var stripe_public_key = $('#id_stripe_public_key').text().slice(1, -1);
var client_secret = $('#id_client_secret').text().slice(1, -1);
var stripe = Stripe(stripe_public_key);
var elements = stripe.elements();

var style = {
    base: {
        color: '#000',
        fontFamily: 'Lexend Mega, sans-serif',
        fontSize: '16px',
        fontSmoothing: 'antialiased',
        '::placeholder': {
            color: '#cccccc',
        },
    },
    invalid: {
        iconColor: '#FFC7EE',
        color: '#FFC7EE',
    }
};

var card = elements.create('card', {style: style});
card.mount('#card-element');
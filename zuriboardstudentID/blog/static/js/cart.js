var addtocartbtns = document.getElementsByClassName('updatecart')

for (i = 0; i < addtocartbtns.length; i++) {
    addtocartbtns[i].addEventListener('click', function (e){
        var productId = this.dataset.product
        var action = this.dataset.action

        
        console.log('USER:', user)
        if (user == 'AnonymousUser') {
            alert('User is not authenticated')
        } else {
            e.preventDefault();
            updateUserOrder(productId, action)
        }
    })
}

function updateUserOrder(productId, action){

    var url = '/add_to_cart/'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'x-CSRFtoken': csrftoken,
        },
        body: JSON.stringify({'productId': productId, 'action': action})
    })
    .then((response) => {
        return response.json();
    })
    .then((data) => {
        location.reload()
    });
}
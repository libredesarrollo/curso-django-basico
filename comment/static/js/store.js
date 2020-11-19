function setSizeShoppingCart() {
    fetch("/cart_size")
        .then(res => res.json())
        .then(data => {
            count = document.querySelector("#shoppingCart .count")
            if (data.size > 0) {
                count.textContent = data.size
                count.classList.remove("d-none")
            }

        })

    setTimeout(setSizeShoppingCart, 5000);

}

setSizeShoppingCart()


function changeQuantityEvent() {

    //changeQuantityMinus = document.querySelector(".changeQuantityMinus")

    document.querySelectorAll(".changeQuantityMinus").forEach((changeQuantityMinus) => {
        //if (changeQuantityMinus) {
        changeQuantityMinus.addEventListener('click', () => {

            id = changeQuantityMinus.getAttribute('data-id')

            e_quantity = document.querySelector("#e_quantity_" + id);
            e_price = document.querySelector("#e_price_" + id);

            res = parseInt(e_quantity.value) - 1

            if (res < 1) {
                res = 1
            }

            e_quantity.value = res

            changeQuantity(id, res,e_price)


        })
        //}
    })





    //changeQuantityPlus = document.querySelector(".changeQuantityPlus")
    document.querySelectorAll(".changeQuantityPlus").forEach((changeQuantityPlus) => {
        //if (changeQuantityPlus) {
        changeQuantityPlus.addEventListener('click', () => {


            id = changeQuantityPlus.getAttribute('data-id')

            e_quantity = document.querySelector("#e_quantity_" + id);
            e_price = document.querySelector("#e_price_" + id);

            res = parseInt(e_quantity.value) + 1

            e_quantity.value = res

            changeQuantity(id, res, e_price)

        })
        // }
    })

}

changeQuantityEvent()

function changeQuantity(id, quantity, e_price) {
    fetch('/add_to_cart/' + id + "?quantity=" + quantity)
        .then(res => res.json())
        .then((res)=>{
            e_price.textContent = "$"+res.e_price
            document.querySelector("#price").textContent = "$"+res.price
        })
}
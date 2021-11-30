/* jshint esversion: 8 */
/* jshint browser: true */
"use strict;";

function populate_cart(){
    let cart_items = window.localStorage.getItem('local_cart') ? JSON.parse(window.localStorage.getItem('local_cart')) : [];

    let content_div = document.getElementById("card-items");
    content_div.innerHTML = "";

    for(let i=0; i<cart_items.length;++i){
        const{
            id,
            author,
            img_url,
            publication_year,
            publisher,
            amount
        } = cart_items[i];
        // create div tag that contain item's content
        let item_div = document.createElement("div");
        item_div.setAttribute("class", "d-flex flex-row justify-content-between align-items-center p-2 mt-4 px-3");
        item_div.setAttribute("id", `item-${id}`);

        // create div tag that contains image tag
        let img_div = document.createElement("div");
        img_div.setAttribute("class", "mr-1 img-checkout");
        let img_tag = document.createElement("img");
        img_tag.setAttribute("src", `${img_url}`);
        img_div.appendChild(img_tag);
        item_div.appendChild(img_div);

        // create div tag that contains item's name
        let name_div = document.createElement("div");
        name_div.setAttribute("class", "d-flex flex-column align-items-center");
        name_div.innerHTML = name;
        item_div.appendChild(name_div);

        // create div tag that contains item's quantity
        let qty_div = document.createElement("div");
        let label = document.createElement("span");
        label.innerHTML = "Qty:";
        let input_amount = document.createElement("input");
        input_amount.setAttribute("type", "number");
        input_amount.setAttribute("min", "1");
        input_amount.setAttribute("value", amount);
        input_amount.setAttribute("style", "max-width: 3rem");
        input_amount.setAttribute("id", `amount-${id}`);
        qty_div.appendChild(label);
        qty_div.appendChild(input_amount);
        item_div.appendChild(qty_div);

        // create div tag to contain remove item button
        let remove_div = document.createElement("div");
        remove_div.setAttribute("class", "d-flex align-items-center");
        let remove_button = document.createElement("button");
        remove_button.setAttribute("class", "btn btn-outline-danger");
        remove_button.setAttribute("onclick", "removeItem(this)");
        let icon = document.createElement("i");
        icon.setAttribute("class", "bi bi-trash");

        remove_button.appendChild(icon);
        remove_div.appendChild(remove_button);
        item_div.appendChild(remove_div);

        content_div.appendChild(item_div);
    }

}

function removeItem(element){
    let cart_items = window.localStorage.getItem('local_cart') ? JSON.parse(window.localStorage.getItem('local_cart')) : [];
    let itemCard = element.parentElement.parentElement;
    let itemId = itemCard.id.split("-")[1];

    itemCard.parentElement.removeChild(itemCard);
    for(let i=0; i < cart_items.length; ++i){
        const {id} = cart_items[i];
        if (id == itemId){
            cart_items.splice(i,1);
        }
    }
    window.localStorage.setItem('local_cart', JSON.stringify(cart_items));
}

function process_checkout(){
    let completeCheckoutPage = window.location.origin + "/store/complete-checkout";
    window.location.replace(completeCheckoutPage);
    window.localStorage.removeItem('local_cart');
}


window.onload = function() {
    populate_cart();
};

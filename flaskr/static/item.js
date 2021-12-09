/* jshint esversion: 8 */ 
/* jshint browser: true */
"use strict;";

var BASE_URL = window.location.origin + "/api/book/item/";

async function add_to_card(btn){
    let item_id = btn.id;
    let item = await requestData(item_id);
    let local_cart = window.localStorage.getItem("local_cart")? JSON.parse(window.localStorage.getItem("local_cart")) : [];
    
    let local_item = checkContainItem(local_cart, item_id);
    if(local_item == null){
        local_cart.push(item);
    }

    document.getElementById("items-in-cart").innerHTML = local_cart.length;
    window.localStorage.setItem('local_cart', JSON.stringify(local_cart));
    
}

async function requestData(itemId) {
    let item = await fetch(`${BASE_URL}/${itemId}`)
    .then(response => {
        return response.json();
    });
    return item;
}

function checkContainItem(storage, item_id){
    for (let i=0; i<storage.length; ++i){
        if (storage[i].id == item_id){
            return i;
        }
    }
    return null;
}

window.onload = function() {
    let local_cart = window.localStorage.getItem("local_cart")? JSON.parse(window.localStorage.getItem("local_cart")) : [];
    document.getElementById("items-in-cart").innerHTML = local_cart.length;
};


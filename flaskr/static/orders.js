/* jshint esversion: 8 */
/* jshint browser: true */
"use strict;";

var HOST_URL = window.location.origin;

async function populate_orders(){
    let cart_items = await requestData();
    let content_div = document.getElementById("order-items");
    content_div.innerHTML = "";
    let currentTime = Date.now();

    for(let i=0; i<cart_items.length;++i){
        const{
            id,
            img_url,
            title,
            order_time
        } = cart_items[i];

        let dueDate = order_time + 864000;
        let timeRemain = Math.floor((dueDate - order_time)/86400);
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
        let prop_div = document.createElement("div");
        prop_div.setAttribute("class", "d-flex flex-column align-items-center");
        let name_div = document.createElement("div");
        name_div.innerHTML = title;
        prop_div.appendChild(name_div);
        let time_div = document.createElement("div");
        if(timeRemain < 0){
            time_div.innerHTML = "Due date: Overdue";
            time_div.setAttribute("class", "overdue-time");
        }else if (timeRemain == 0){
            time_div.innerHTML = "Due date: Today";
            time_div.setAttribute("class", "due-time");
        }else{
            time_div.innerHTML = `Due date: ${Date(dueDate).toLocaleString()}`;
            time_div.setAttribute("class", "due-time");
        }
        prop_div.appendChild(time_div);
        item_div.appendChild(prop_div);

        // create div tag to contain remove item button
        let remove_div = document.createElement("div");
        remove_div.setAttribute("class", "d-flex align-items-center");
        let remove_button = document.createElement("button");
        remove_button.setAttribute("class", "btn btn-outline-danger");
        remove_button.setAttribute("onclick", "returnItem(this)");

        remove_button.innerHTML = "Return";
        remove_div.appendChild(remove_button);
        item_div.appendChild(remove_div);

        content_div.appendChild(item_div);
    }

}

async function returnItem(element){
    let orderCard = element.parentElement.parentElement;
    let orderId = orderCard.id.split("-")[1];
    let apiEndPoint = HOST_URL + `/api/book/orders/delete/${orderId}`;
    let delete_response = await fetch(apiEndPoint, {method: "DELETE"});

    if(delete_response.status === 200){
        orderCard.parentElement.removeChild(orderCard);
    }
}

async function requestData() {
    let item = await fetch(HOST_URL + '/api/book/orders')
    .then(response => {
        return response.json();
    });
    return item;
}

window.onload = function() {
    populate_orders();
};

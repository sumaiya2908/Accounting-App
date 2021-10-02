let cartBtn = document.querySelectorAll(".add-to-cart");
let cart = [];
let quantity = 0;
cartBtn.forEach((btn) => {
	btn.onclick = function (event) {
		item = btn.dataset;
		if (cart.length > 0) {
			if (!cart.some((cart_item) => cart_item.name == item.name)) {
				addItem(item);
			} else {
				item = cart.find((cart_item) => cart_item.name == item.name);
				item["quantity"] += 1;
				item["total_price"] *= item["quantity"];
			}
		} else {
			addItem(item);
		}
		quantity += 1;
		document.querySelector(".badge").innerHTML = quantity;
		localStorage.setItem("cart", JSON.stringify(cart));
		localStorage.setItem('quantity', quantity)
	};
});

function addItem(item) {
	let new_item = {};
	new_item["name"] = item.name;
	new_item["price"] = item.price;
	new_item["total_price"] = item.price;
	new_item["quantity"] = 1;
	cart.push(new_item);
}

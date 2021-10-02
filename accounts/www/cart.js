let cart = JSON.parse(localStorage["cart"]);
let quantity = localStorage["quantity"];
document.querySelector(".badge").innerHTML = quantity;
let cart_div = document.querySelector(".cart-container");

if (cart.length == 0) {
	cart.innerHTML = "Cart is Empty";
} else {
	cart.map((item) => {
		let cart_item =
			'<div class="row w-100"><span class="col-sm font-weight-bold">' +
			item.name +
			'</span><span class="col-sm">'+
			item.price +
			'</span><span class="col-sm">' +
			item.quantity +
			'</span><span class="col-sm">' +
			item.total_price +
			'</span></div><hr>';
		cart_div.insertAdjacentHTML("beforeend", cart_item);
	});
	btn = '<div class="w-100 text-right p-5"><button class="btn btn-primary checkout-btn">Checkout Invoice</button></div>'
	cart_div.insertAdjacentHTML('afterend', btn)
}

let cart_btn = document.querySelectorAll(".cart-btn");
document.querySelector('.checkout-btn').onclick = function () {
	frappe.call({
        method: 'accounts.accounts.doctype.sales_invoice.sales_invoice.generate_sales_invoice',
        args: {
            'data' : JSON.stringify(cart),
			'company': 'Gada Electronics'
        },
        callback: function(r) {
            openPDF('Sales Invoice', r.message, 'pdf')
        }
    });
}


function openPDF(doc, docname, type) {
	let full_pdf_url = get_full_url(
        '/printview?doctype=' +
        encodeURIComponent(doc) +
        '&name=' +
        encodeURIComponent(docname) +
        '&trigger_print=1' +
        '&format=' +
		encodeURIComponent(type)
    )
	const w = window.open(full_pdf_url)
}

function get_full_url(url) {
    if(url.indexOf("http://")===0 || url.indexOf("https://")===0) {
        return url;
    }
    return url.substr(0,1)==="/" ?
        (get_base_url() + url) :
        (get_base_url() + "/" + url);
}

function get_base_url() {
    let url = (frappe.base_url || window.location.origin);
    if(url.substr(url.length-1, 1)=='/') url = url.substr(0, url.length-1);
    return url;
}
console.log(2+3)

document.querySelector("#rr_submit").addEventListener("click", async () => {
  const data = {
    item_name: document.querySelector("#rr_itemname").value,
    item_quantity: document.querySelector("#rr_itemquantity").value,
    item_status: document.querySelector("#rr_status").value,
    date: document.querySelector("#rr_date").value,

    console.log(item_name);
    console.log(item_quantity);
    console.log(item_status);
    console.log(date);
  };

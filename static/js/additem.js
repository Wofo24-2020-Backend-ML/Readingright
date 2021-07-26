console.log(2+3)

document.querySelector("#rr_submit").addEventListener("click", async () => {
  const data = {
    item_name: document.querySelector("#rr_itemname").value,
    item_quantity: document.querySelector("#rr_itemquantity").value,
    item_status: document.querySelector("#rr_status").value,
    date: document.querySelector("#rr_date").value,
  };


  const response = await axios.post(
    "https://readingrighttried1.herokuapp.com/api/additem/",
    {
    headers: {
        "Content-Type": "application/json",
        "Authorization": 'Bearer' + localStorage.getItem('Bearer')}},
    data
  );
  console.log(response);
  console.log(item_name)
});


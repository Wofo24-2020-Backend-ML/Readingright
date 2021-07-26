console.log(2+3);

document.querySelector("#rr_submit").addEventListener("click", async () => {
  const data = {
    name: document.querySelector("#rr_name").value,
    phone_number: document.querySelector("#rr_phone").value,
    email: document.querySelector("#rr_email").value,
    password: document.querySelector("#rr_password").value,
  };
  const response = await axios.post(
    "https://readingrighttried1.herokuapp.com/createuser/",
    data
  );
  console.log(response);
});

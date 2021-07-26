document.querySelector("#rr_submit").addEventListener("click", async () => {
  const data = {
    phone_number: document.querySelector("#rr_phone").value,
    password: document.querySelector("#rr_password").value,
  };
  const response = await axios.post(
    "https://readingrighttried1.herokuapp.com/login/",
    data
  );
  console.log(response);
  console.log(response.data.access);
  localStorage.setItem("Bearer", response.data.access);
});

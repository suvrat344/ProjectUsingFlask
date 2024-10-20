function toggleFields()
{
  role = document.querySelector(".role")
  customer_field = document.getElementById("customer")
  professional_field = document.getElementById("professional")

  if(role.value === "Customer")
  {
    console.log("1")
    customer_field.style.display = "block";
    professional_field.style.display = "none"
  }
  else if(role.value === "Professional")   
  {
    console.log("2")
    customer_field.style.display = "none";
    professional_field.style.display = "block";
  }
  else
  {
    customer_field.style.display = "none";
    professional_field.style.display = "none";
  }
}
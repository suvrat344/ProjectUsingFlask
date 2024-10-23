function toggleFields()
{
  let role = document.querySelector(".role")
  let customer_field = document.getElementById("customer")
  let professional_field = document.getElementById("professional")

  if(role.value === "Customer")
  {
    customer_field.style.display = "block";
    professional_field.style.display = "none"
    document.getElementById("address").required = true;
    document.getElementById("experience").required = false;
    document.getElementById("specialization").required = false;
  }
  else if(role.value === "Professional")   
  {
    customer_field.style.display = "none";
    professional_field.style.display = "block";
    document.getElementById("address").required = false;
    document.getElementById("experience").required = true;
    document.getElementById("specialization").required = true;
  }
  else
  {
    customer_field.style.display = "none";
    professional_field.style.display = "none";
    document.getElementById("address").required = false;
    document.getElementById("experience").required = false;
    document.getElementById("specialization").required = false;
  }
}


function setTodayDate()
{
  const request_date = document.getElementById("request_date");
  if(request_date)
  {
    const today = new Date().toISOString().split('T')[0];
    request_date.value = today;
  }
}

window.onload = setTodayDate;
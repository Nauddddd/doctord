const menuToggle = document.querySelector('.toggle');
const showcase = document.querySelector('.showcase');
const backBtn0 = document.querySelector('#btn0');
const backBtn1 = document.querySelector('#btn1') ;

menuToggle.addEventListener('click', () => {
  menuToggle.classList.toggle('active');
  showcase.classList.toggle('active');
  if(backBtn1.style.display === "none"){
    backBtn1.style.display = null;
  }else{
    backBtn1.style.display = "none";
  }
})

backBtn0.addEventListener('click', () => {
  menuToggle.classList.toggle('active');
  showcase.classList.toggle('active');
})
if ( backBtn1 != null){
  backBtn1.addEventListener('click', () => {
    location.href = '../history';
  })
}


// --------------------------------------------------------------
var check = function() {
  if (document.getElementById('password').value ==
    document.getElementById('confirm_password').value) {
    document.getElementById('message').style.color = 'green';
    document.getElementById('message').innerHTML = '✓';
  } else {
    document.getElementById('message').style.color = 'red';
    document.getElementById('message').innerHTML = '✗';
  }
}

// =================================================================
function validateEmail(email) 
    {
        var re = /\S+@\S+\.\S+/;
        return re.test(email);
    }
function onChange() {
  const password = document.querySelector('input[name=password]');
  const confirm = document.querySelector('input[name=confirm_password]');
  const email = document.getElementById("email");
  if (!(validateEmail(email.value))) {
    email.setCustomValidity("I am expecting an e-mail address!");
  }
  else if (confirm.value === password.value) {
    confirm.setCustomValidity('');
  } else {
    confirm.setCustomValidity('Passwords do not match');
  }
}
// ====================================================================
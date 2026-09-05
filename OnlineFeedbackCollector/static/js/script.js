function validateForm() {
  const rating = document.querySelector('input[name="rating"]:checked');
  if (!rating) {
    alert("Please select a rating from 1 to 5.");
    return false;
  }
  return true;
}

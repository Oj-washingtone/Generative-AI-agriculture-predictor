// Check if the session variable is set to false (indicating the user has completed onboarding)
const sessionVariable = sessionStorage.getItem("onboardingCompleted");

// If the session variable is not set or is set to false, show the overlay
if (sessionVariable === null || sessionVariable === "false") {
  const overlay = document.getElementById("onboarding-overlay");
  overlay.style.display = "flex";
}

function closeOverlay() {
  const overlay = document.getElementById("onboarding-overlay");
  overlay.style.display = "none";

  // Set the session variable to indicate onboarding is completed
  sessionStorage.setItem("onboardingCompleted", "true");
}
// Example: Close the overlay when the user clicks a button with the ID "get-started-button"
const getStartedButton = document.getElementById("get-started-button");
getStartedButton.addEventListener("click", closeOverlay);

// Check if the session variable is set to false if the user refreshes the page or navigates away and back to the page (indicating the user has completed onboarding) and close the overlay if it is set to false
window.addEventListener("load", () => {
  const sessionVariable = sessionStorage.getItem("onboardingCompleted");
  if (sessionVariable === "true") {
    closeOverlay();
  }
});

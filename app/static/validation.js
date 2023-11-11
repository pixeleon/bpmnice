const INVALID_NAME_CHARACTERS_REGEX = /[!@#$%^&*()_+={}[\]:;<>,.?/~\\]/;
const EMAIL_REGEX = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

function validateSignupForm() {
    const nameInput = document.getElementById('signupNameInput');
    const nameValue = nameInput.value.trim();
    const nameInputFeedback = document.getElementById('signupNameInputFeedback');

    const emailInput = document.getElementById('signupEmailInput');
    const emailValue = emailInput.value.trim();
    const emailInputFeedback = document.getElementById('signupEmailInputFeedback');

    const passwordInput = document.getElementById('signupPasswordInput');
    const passwordValue = passwordInput.value.trim();
    const passwordInputFeedback = document.getElementById('signupPasswordInputFeedback');

    nameInput.classList.remove('is-invalid');
    emailInput.classList.remove('is-invalid');
    passwordInput.classList.remove('is-invalid');

    if (nameValue === '') {
        nameInput.classList.add('is-invalid');
        nameInputFeedback.textContent = 'Must not be empty';
        return false;
    }

    if (nameValue.length < 2) {
        nameInput.classList.add('is-invalid');
        nameInputFeedback.textContent = 'Must be at least 2 characters';
        return false;
    }

    if (nameValue.length > 50) {
        nameInput.classList.add('is-invalid');
        nameInputFeedback.textContent = 'Must be at most 50 characters';
        return false;
    }

    if (/\d/.test(nameValue)) {
        nameInput.classList.add('is-invalid');
        nameInputFeedback.textContent = 'Cannot contain any numerals';
        return false;
    }

    if (INVALID_NAME_CHARACTERS_REGEX.test(nameValue)) {
        nameInput.classList.add('is-invalid');
        nameInputFeedback.textContent = 'Cannot contain special characters other than space, hyphen, and apostrophe';
        return false;
    }

    nameInput.value = nameValue;

    if (emailValue === '') {
        emailInput.classList.add('is-invalid');
        emailInputFeedback.textContent = 'Must not be empty';
        return false;
    }

    if (emailValue.length < 8) {
        emailInput.classList.add('is-invalid');
        emailInputFeedback.textContent = 'Must be at least 8 characters';
        return false;
    }

    if (emailValue.length > 100) {
        emailInput.classList.add('is-invalid');
        emailInputFeedback.textContent = 'Must be at most 100 characters';
        return false;
    }

    if (!EMAIL_REGEX.test(emailValue)) {
        emailInput.classList.add('is-invalid');
        emailInputFeedback.textContent = 'Must be a valid email address';
        return false;
    }

    emailInput.value = emailValue;

    if (passwordValue === '') {
        passwordInput.classList.add('is-invalid');
        passwordInputFeedback.textContent = 'Must not be empty';
        return false;
    }

    if (passwordValue.length < 8) {
        passwordInput.classList.add('is-invalid');
        passwordInputFeedback.textContent = 'Must be at least 8 characters';
        return false;
    }

    if (passwordValue.length > 100) {
        passwordInput.classList.add('is-invalid');
        passwordInputFeedback.textContent = 'Must be at most 100 characters';
        return false;
    }

    if (!/\d/.test(passwordValue)) {
        passwordInput.classList.add('is-invalid');
        passwordInputFeedback.textContent = 'Must contain at least one digit';
        return false;
    }

    if (!/[\W_]/.test(passwordValue)) {
        passwordInput.classList.add('is-invalid');
        passwordInputFeedback.textContent = 'Must contain at least one special character';
        return false;
    }

    passwordInput.value = passwordValue;

    return true;
}

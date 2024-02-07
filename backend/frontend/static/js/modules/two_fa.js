import { getCookie } from "./utils.js";

async function enable2fa() {
	try {
		const csrfToken = getCookie('csrftoken');
		const accessToken = localStorage.getItem('jwt_token');
		const baseURL = window.location.protocol + '//' + window.location.hostname + (window.location.port ? ':' + window.location.port : '');

		// Request a new 2FA setup for the current user
		const response = await fetch(`${baseURL}/api/enable_2fa`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken': csrfToken,
			'Authorization': `Bearer ${accessToken}`,
		},
		credentials: 'include',
		});
 
		if (response.ok) {
			const data = await response.json();

			if (data.success) {
				// Generate the OTP URL
				const otpauthUrl = data.otpauth_url;
				displayQRCode(otpauthUrl);
			}
			else {
				console.error('Error enabling 2FA:', data.error);
			}
		}
		else {
			console.error('Error enabling 2FA:', response.status);
		}
	}
	catch (error) {
		console.error('Error enabling 2FA:', error);
	}
}

function displayQRCode(otpauthUrl) {
	const qrCodeContainer = document.getElementById('qrcode'); // Replace with your container ID

	// Construct the data URI for the QR code image
	const dataUri = `https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=${encodeURIComponent(otpauthUrl)}`;

	// Create the qr code
	const imgElement = document.createElement('img');
	imgElement.src = dataUri;
	qrCodeContainer.innerHTML = '';
	qrCodeContainer.appendChild(imgElement);

	console.log('QR code generated successfully.');
}

async function disable2fa() {
	try {
		const csrfToken = getCookie('csrftoken');
		const accessToken = localStorage.getItem('jwt_token');
		const baseURL = window.location.protocol + '//' + window.location.hostname + (window.location.port ? ':' + window.location.port : '');

		const response = await fetch(`${baseURL}/api/disable_2fa`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken': csrfToken,
			'Authorization': `Bearer ${accessToken}`,
		},
		credentials: 'include',
		});
 
		if (response.ok) {
			const data = await response.json();
			const qrCodeContainer = document.getElementById('qrcode');
			qrCodeContainer.innerHTML = '';
			console.log('2FA disabled successfully:', data.message);	
		}
		else {
			console.error('Error disabling 2FA:', response.status);
		}
	}
	catch (error) {
		console.error('Error disabling 2FA:', error);
	}
}

async function check2faStatus() {
    try {
        const csrfToken = getCookie('csrftoken');
        const accessToken = localStorage.getItem('jwt_token');
        const baseURL = window.location.protocol + '//' + window.location.hostname + (window.location.port ? ':' + window.location.port : '');
		const switchbox2FA = document.getElementById('switchbox2FA');
        const response = await fetch(`${baseURL}/api/get_2fa_status`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
                'Authorization': `Bearer ${accessToken}`,
            },
            credentials: 'include',
        });

        if (response.ok) {
            const data = await response.json();
            if (data.two_factor_enabled) {
                console.log('IF CHECK2FASTATUS');
                switchbox2FA.checked = true
            }
			else {
                console.log('ELSE CHECK2FASTATUS');
                switchbox2FA.checked = false
            }
        }
		else {
            console.error('Error checking 2FA status:', response.status);
        }
    }
	catch (error) {
        console.error('Error checking 2FA status:', error);
    }
}

export { enable2fa, disable2fa, check2faStatus }
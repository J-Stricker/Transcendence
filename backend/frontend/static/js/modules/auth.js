import { getCookie, makeApiRequest } from './utils.js'
import { displayLoginPage, displayHomePage } from './display_page_function.js'
import { state } from '../main.js';

async function fetchCode(code, state) {
    try {
        await makeApiRequest("get_csrf_token");
        const csrfToken = getCookie('csrftoken');
        const baseURL = window.location.protocol + '//' + window.location.hostname + (window.location.port ? ':' + window.location.port : '');
        const response = await fetch(`${baseURL}/api/auth42`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify({ code: code, state: state}),
            credentials: 'include',
        })
        if (response.ok) {
            // const data = await response.json();
            displayHomePage();
        }
        else {
            console.error('Error login user:', response.status);
            displayLoginPage();
        }
    }
    catch (error) {
        console.error('Error login user:', error);
        displayLoginPage();
    }
}

async function checkAuth42() {
    var url = window.location;
    var urlSearch = window.location.search;
    var urlSearchParams = new URLSearchParams(urlSearch);
    var urlPathname = window.location.pathname;
    var totalPath = urlPathname + urlSearch;

    // Vérifie si l'URL contient "/home"
    if (!totalPath.match(/^\/home/)) {
        return;
    }
    // Vérifie si la partie parser.search ne commence pas par "error"
    if (!urlSearch.startsWith("?code")) {
        return;
    }
    var codeValue = urlSearchParams.get("code");
    var stateValue = urlSearchParams.get("state");
    console.log("state : ", state)
    console.log("stateValue : ", stateValue)
    console.log("params : ", urlSearchParams.size)
    if (urlSearchParams.size !== 2 && stateValue !== state)
    {
        console.log("ici")
        displayLoginPage();
        return;
    }
    await fetchCode(codeValue, stateValue);
}

export { checkAuth42 };

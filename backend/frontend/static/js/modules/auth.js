import { getCookie } from './utils.js'
import { displayLoginPage, displayHomePage } from './display_page_function.js'

async function fetchCode(code, state) {
    try {
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
            const data = await response.json();
        }
        else {
            console.error('Error login user:', response.status);
        }
    }
    catch (error) {
        console.error('Error login user:', error);
    }
}

async function checkAuth42() {
    var url = window.location;
    var urlSearch = window.location.search;
    var urlSearchParams = new URLSearchParams(urlSearch);
    var urlPathname = window.location.pathname;
    console.log('url', url);
    console.log('urlPathname', urlPathname);
    console.log('urlSearchParams', urlSearchParams);
    console.log('urlSearch', urlSearch);
    var totalPath = urlPathname + urlSearch;
    console.log('totalPath', totalPath);

    // Vérifie si l'URL contient "/home"
    if (!totalPath.match(/^\/home/)) {
        console.log("L'URL n'est pas valide.");
        return;
    }

    // Vérifie si la partie parser.search ne commence pas par "error"
    if (!urlSearch.startsWith("?code")) {
        console.log("La recherche commence par 'error', donc la fonction retourne.");
        return;
    }

    var codeValue = urlSearchParams.get("code");
    var stateValue = urlSearchParams.get("state");
    if (urlSearchParams.size !== 2 && stateValue !== state)
    {
        console.log("Pas assez de param, donc la fonction retourne.");
        displayLoginPage();
        return;
    }
    await fetchCode(codeValue, stateValue);
	displayHomePage();
}

export { checkAuth42 };

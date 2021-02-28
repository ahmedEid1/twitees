    document.querySelector('#follow').onclick = (e) => follow(e);
    document.querySelector('#unfollow').onclick = (e) => unFollow(e);

    console.log("here")

function follow(e) {
    const user = e.target.dataset['user'];
    const follow = e.target.dataset['profile'];

    fetch(`/follow/${user}/${follow}`).then(() => e.target.innerHTML = 'Unfollow');
}

function unFollow(e) {
    const user = e.target.dataset['user'];
    const follow = e.target.dataset['profile'];

    fetch(`/unfollow/${user}/${follow}`).then(() => e.target.innerHTML = 'Follow');
}
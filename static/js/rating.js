function setStars(className, rating) {
    console.log('test')
    let selected = ['fa-solid', 'checked']
    let unselected = ['fa-regular', 'unchecked']
    let halfSelected = ['fa-solid', 'fa-solid', 'fa-star-half', 'checked']

    let stars = document.getElementsByClassName(className)
    let i = 0;
    let num = stars.length / 5
    while (num > 0) { // For multiple occurrences of the same review
        let r = rating
        while (r > 0) {
            if (r >= 1) {
                stars[i].classList.add(...selected)
                stars[i].classList.remove(...unselected)
            } else {
                stars[i].classList.add(...halfSelected)
                stars[i].classList.remove(...unselected)
            }
            i++
            r--
        }
        i = (i - i%5) + 5
        num--
    }

}
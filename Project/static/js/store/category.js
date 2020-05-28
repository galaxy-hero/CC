class Category{
    constructor(list){
        this.list;
    }

    render(data) {
        const html = `
        <li class="item">
            <span>item1</span>
        </li>
        `;
        this.list.innerHTML += html;
    }
}


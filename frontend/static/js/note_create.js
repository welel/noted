$(function() {


    $('#id_source').selectize({
        maxItems: 1,
        valueField: "id",
        labelField: "title",
        searchField: ["title"],
        create: true,
        placeholder: gettext('Source name...'),

        load: (query, callback) => {
            if(!query.length) return callback();
            $.ajax({
                url: 'http://127.0.0.1:8000/en/search-sources-select/',
                type: 'GET',
                dataType: 'json',
                data: {'query': query},
                success: (res) => {
                    console.log(res);
                    callback(res.data);
                },
                error: () => callback(),
            });
        },

        render: {
            option: (item, escape) => {
                return '<p class="fs-5 p-2"><span id="source_type_' + item.id +
                        '" name="' + item.type[0] + '" class="badge rounded-pill text-bg-success me-2">' + 
                        item.type[1] + '</span>' + item.title + '</p>';
            }
        },

        onItemAdd: (id) => {
            const typeElemetnt = $('#id_source_type')[0];
            typeElemetnt.value = $('#source_type_' + id)[0].getAttribute('name');
        },
    });


});

$(document).ready(function () {
    // Function to fetch categories and subcategories
    function updatePaginationLinks() {
        // Reattach event listeners for pagination links
        $('#pagination-links .page-link').on('click', function (e) {
            e.preventDefault();
            var pageUrl = $(this).attr('href');
            fetchProducts(pageUrl); // Call a function to fetch products based on the URL
        });
    }

    function fetchCategoriesAndSubcategories() {
        $.ajax({
            url: categoriesUrl,
            type: "GET",
            success: function (response) {
                // Populate categories dropdown
                response.categories.forEach(function (category) {
                    $('#category').append($('<option>', {
                        value: category.id,
                        text: category.name
                    }));
                });

                // Populate subcategories dropdown
                response.subcategories.forEach(function (subcategory) {
                    $('#subcategory').append($('<option>', {
                        value: subcategory.id,
                        text: subcategory.name
                    }));
                });
            },
            error: function (xhr, errmsg, err) {
                console.log(errmsg);
                // Handle error if necessary
            }
        });
    }
    function filterProducts(formData) {
        $.ajax({
            url: filterUrl,
            type: "GET",
            data: formData,
            success: function (response) {
                var filteredProductsContainer = $('#filteredProductsContainer');
                filteredProductsContainer.empty(); // Clear previous products in the container

                // Create and append product cards to the existing container
                response.products.forEach(function (product) {
                    var productCard =
                        '<div class="col-md-4 mb-4">' +
                        '<div class="card h-100">' +
                        '<div class= "imgBox">' +
                        (product.image_url ? '<img class="card-img-top product-image" src="' + product.image_url + '" alt="' + product.name + '">' : '<span>No Image Available</span>') +
                        '</div>' +
                        '<div class="contentBox text-center">' +
                        '<h5 class="card-title">' + product.subcategory + ' ' + product.name + '</h5>' +
                        '<h6 class="card-title">' + product.category + '</h6>' +
                        '<p class="card-text">' + product.price + '€</p>' +

                        '</div></div></div>';

                    filteredProductsContainer.append(productCard);
                });
            },

            error: function (xhr, errmsg, err) {
                console.log(errmsg);
                // Handle error if necessary
            }
        });
    }
    fetchCategoriesAndSubcategories(); // Fetch categories and subcategories on page load

    $('#filter-form').submit(function (event) {
        event.preventDefault(); // Prevent default form submission

        var formData = $(this).serialize();
        filterProducts(formData); // Call the function to filter products
    });
    $('#pagination-links').html(response.pagination_html);

    // Reinitialize event listeners for pagination links
    updatePaginationLinks();
});
$('.rating-stars .star').on('click', function () {
    var value = $(this).data('value');
    var productId = '{{ product.id }}';  // Pass the product ID here
    var csrfToken = '{{ csrf_token }}';
    $.ajax({
        url: '/rate-product/',  // Replace with your rating view URL
        method: 'POST',
        data: {
            'product_id': productId,
            'stars': value
        },
        success: function (response) {
            // Handle success (e.g., update UI)
        },
        error: function (xhr, errmsg, err) {
            console.log(errmsg);
            // Handle error if necessary
        }
    });
});
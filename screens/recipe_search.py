import streamlit as st
import requests
import math

def load_local_css():
    pass

def get_ingredients(meal):
    """Extract ingredients and measurements from meal data"""
    ingredients = []
    for i in range(1, 21):  # TheMealDB provides up to 20 ingredients
        ingredient = meal.get(f"strIngredient{i}")
        measure = meal.get(f"strMeasure{i}")
        if ingredient and ingredient.strip():
            ingredients.append(f"{measure} {ingredient}".strip())
    return ingredients

def display_pagination(current_page, total_pages):
    """Display pagination buttons"""
    st.markdown('<div class="pagination">', unsafe_allow_html=True)
    
    # Previous button
    prev_disabled = "disabled" if current_page == 1 else ""
    st.markdown(
        f'<button class="page-button {prev_disabled}" '
        f'onclick="window.location.href=\'?page={current_page-1}\'">&laquo; Previous</button>',
        unsafe_allow_html=True
    )
    
    # Page number buttons
    for i in range(1, total_pages + 1):
        active = "active" if i == current_page else ""
        st.markdown(
            f'<button class="page-button {active}" '
            f'onclick="window.location.href=\'?page={i}\'">{i}</button>',
            unsafe_allow_html=True
        )
    
    # Next button
    next_disabled = "disabled" if current_page == total_pages else ""
    st.markdown(
        f'<button class="page-button {next_disabled}" '
        f'onclick="window.location.href=\'?page={current_page+1}\'">Next &raquo;</button>',
        unsafe_allow_html=True
    )
    
    st.markdown('</div>', unsafe_allow_html=True)

def run():
    
    # Initialize session state if not already done
    if 'page' not in st.session_state:
        st.session_state.page = 1
    if 'meals' not in st.session_state:
        st.session_state.meals = []
    if 'detailed_view' not in st.session_state:
        st.session_state.detailed_view = False
    if 'selected_meal_id' not in st.session_state:
        st.session_state.selected_meal_id = None
    if 'search_performed' not in st.session_state:
        st.session_state.search_performed = False
    
    # App header
    st.markdown('<h1 class="title">🍽️ Gourmet Recipe Finder</h1>', unsafe_allow_html=True)
    
    # If we're in detailed view, show the recipe details
    if st.session_state.detailed_view:
        display_recipe_detail()
        return
    
    # Otherwise, show the search interface and recipe cards
    st.markdown("""
    <p style="text-align: center;">Discover delicious recipes from around the world. 
    Search by name or ingredient to find your next culinary adventure!</p>
    """, unsafe_allow_html=True)
    
    # Sidebar for search options
    with st.sidebar:
        st.markdown('<h3 class="section-header">Search Options</h3>', unsafe_allow_html=True)
        search_type = st.radio("Search by:", ["Recipe Name", "Main Ingredient"])
        cuisine_filter = st.selectbox(
            "Filter by Cuisine (Optional):", 
            ["Any", "American", "British", "Canadian", "Chinese", "French", "Indian", "Italian", "Japanese", "Mexican", "Thai"]
        )
        st.markdown('<div class="footer">Data provided by TheMealDB</div>', unsafe_allow_html=True)
    
    # Main search interface
    search_placeholder = "Enter recipe name..." if search_type == "Recipe Name" else "Enter main ingredient..."
    query = st.text_input(search_placeholder, key="search_box")
    
    # When search button is clicked or query changes
    search_button = st.button("Search")
    if search_button or (query and not st.session_state.search_performed):
        st.session_state.search_performed = True
        st.session_state.page = 1  # Reset to first page on new search
        
        with st.spinner('Searching for delicious recipes...'):
            # Determine the API endpoint based on search type
            if search_type == "Recipe Name":
                url = f"https://www.themealdb.com/api/json/v1/1/search.php?s={query}"
            else:
                url = f"https://www.themealdb.com/api/json/v1/1/filter.php?i={query}"
            
            res = requests.get(url)
            data = res.json()
            meals = data.get("meals", [])
            
            # Filter by cuisine if selected
            if cuisine_filter != "Any" and meals:
                filtered_meals = []
                for meal_basic in meals:
                    # Get full meal details to check cuisine
                    meal_id = meal_basic["idMeal"]
                    meal_url = f"https://www.themealdb.com/api/json/v1/1/lookup.php?i={meal_id}"
                    meal_res = requests.get(meal_url)
                    meal_full = meal_res.json().get("meals", [{}])[0]
                    
                    if meal_full.get("strArea") == cuisine_filter:
                        filtered_meals.append(meal_full)
                
                st.session_state.meals = filtered_meals
            else:
                st.session_state.meals = meals
    
    # Display search results if there are any
    if st.session_state.meals:
        display_recipe_cards()
    elif st.session_state.search_performed:
        st.warning(f"No recipes found for '{query}'. Try a different search term.")

def display_recipe_cards():
    """Display recipe cards with pagination"""
    meals = st.session_state.meals
    total_meals = len(meals)
    
    st.markdown(f"<h3 class='section-header'>Found {total_meals} recipes</h3>", unsafe_allow_html=True)
    
    # Pagination parameters
    items_per_page = 8
    total_pages = math.ceil(total_meals / items_per_page)
    current_page = st.session_state.page
    
    # Ensure current page is valid
    if current_page < 1:
        current_page = 1
    if current_page > total_pages:
        current_page = total_pages
    
    st.session_state.page = current_page
    
    # Calculate slice indices for current page
    start_idx = (current_page - 1) * items_per_page
    end_idx = min(start_idx + items_per_page, total_meals)
    
    # Display pagination controls
    if total_pages > 1:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            # Custom pagination UI
            pagination_html = '<div class="pagination">'
            
            # Previous button
            prev_disabled = "disabled" if current_page == 1 else ""
            pagination_html += f'<span class="page-button {prev_disabled}" '
            if current_page > 1:
                pagination_html += f'onclick="this.dispatchEvent(new CustomEvent(\'click\'))"'
            pagination_html += '>&laquo;</span>'
            
            # Page number buttons
            for i in range(1, total_pages + 1):
                active = "active" if i == current_page else ""
                pagination_html += f'<span class="page-button {active}" '
                pagination_html += f'onclick="this.dispatchEvent(new CustomEvent(\'click\'))">{i}</span>'
            
            # Next button
            next_disabled = "disabled" if current_page == total_pages else ""
            pagination_html += f'<span class="page-button {next_disabled}" '
            if current_page < total_pages:
                pagination_html += f'onclick="this.dispatchEvent(new CustomEvent(\'click\'))"'
            pagination_html += '>&raquo;</span>'
            
            pagination_html += '</div>'
            st.markdown(pagination_html, unsafe_allow_html=True)
            
            # Handle pagination clicks with regular buttons
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                if st.button("◀ Previous", disabled=(current_page == 1)):
                    st.session_state.page -= 1
                    st.rerun()
            with col3:
                if st.button("Next ▶", disabled=(current_page == total_pages)):
                    st.session_state.page += 1
                    st.rerun()
    
    # Display recipe cards for current page
    current_meals = meals[start_idx:end_idx]
    
    # Create 4 columns for the grid
    for i in range(0, len(current_meals), 4):
        cols = st.columns(4)
        
        # Add a recipe card to each column
        for j in range(4):
            if i + j < len(current_meals):
                meal = current_meals[i + j]
                with cols[j]:
                    # Create clickable card
                    meal_id = meal["idMeal"]
                    
                    # Check if we need to fetch full details
                    if "strInstructions" not in meal:
                        # Store only basic info until detailed view
                        basic_info = True
                    else:
                        basic_info = False
                    
                    card_html = f"""
                    <div class="recipe-card" onclick="this.dispatchEvent(new CustomEvent('click'))">
                        <div class="card-img-container">
                            <img src="{meal['strMealThumb']}" class="card-img" alt="{meal['strMeal']}">
                        </div>
                        <h3 class="recipe-title">{meal['strMeal']}</h3>
                    </div>
                    """
                    
                    st.markdown(card_html, unsafe_allow_html=True)
                    
                    # Hidden button to handle click
                    if st.button(f"View {meal['strMeal']}", key=f"meal_{meal_id}"):
                        st.session_state.detailed_view = True
                        st.session_state.selected_meal_id = meal_id
                        st.session_state.is_basic_info = basic_info
                        st.rerun()
    
    # Show pagination at the bottom if there are multiple pages
    if total_pages > 1:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            page_text = f'<p style="text-align: center;">Page {current_page} of {total_pages}</p>'
            st.markdown(page_text, unsafe_allow_html=True)

def display_recipe_detail():
    """Display detailed view of a recipe"""
    meal_id = st.session_state.selected_meal_id
    
    # Add back button
    if st.button("← Back to Search Results"):
        st.session_state.detailed_view = False
        st.rerun()
    
    # Fetch detailed recipe information if needed
    if hasattr(st.session_state, 'is_basic_info') and st.session_state.is_basic_info:
        url = f"https://www.themealdb.com/api/json/v1/1/lookup.php?i={meal_id}"
        response = requests.get(url)
        data = response.json()
        meal = data.get("meals", [{}])[0]
    else:
        # Find the meal in the existing list
        meal = next((m for m in st.session_state.meals if m["idMeal"] == meal_id), None)
        if not meal:
            url = f"https://www.themealdb.com/api/json/v1/1/lookup.php?i={meal_id}"
            response = requests.get(url)
            data = response.json()
            meal = data.get("meals", [{}])[0]
    
    # Display detailed recipe
    st.markdown(f'<div class="detail-container">', unsafe_allow_html=True)
    
    # Recipe title
    st.markdown(f'<h1 class="recipe-title">{meal["strMeal"]}</h1>', unsafe_allow_html=True)
    
    # Tags section
    tags_html = ""
    if meal.get("strArea"):
        tags_html += f'<span class="tag">{meal["strArea"]}</span>'
    if meal.get("strCategory"):
        tags_html += f'<span class="tag">{meal["strCategory"]}</span>'
    if meal.get("strTags") and meal["strTags"] not in ["null", "", None]:
        for tag in meal["strTags"].split(","):
            if tag.strip():
                tags_html += f'<span class="tag">{tag.strip()}</span>'
    
    if tags_html:
        st.markdown(f'<div style="text-align: center; margin-bottom: 20px;">{tags_html}</div>', unsafe_allow_html=True)
    
    # Main image
    st.markdown(f'<img src="{meal["strMealThumb"]}" class="centered-image" width="400">', unsafe_allow_html=True)
    
    # Ingredients and Instructions in columns
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown('<h3 class="section-header">Ingredients</h3>', unsafe_allow_html=True)
        ingredients = get_ingredients(meal)
        ingredients_html = "<div class='ingredient-list'><ul>"
        for ingredient in ingredients:
            ingredients_html += f"<li>{ingredient}</li>"
        ingredients_html += "</ul></div>"
        st.markdown(ingredients_html, unsafe_allow_html=True)
    
    with col2:
        st.markdown('<h3 class="section-header">Instructions</h3>', unsafe_allow_html=True)
        instructions = meal["strInstructions"].replace("\n", "<br>")
        st.markdown(f'<div class="instructions">{instructions}</div>', unsafe_allow_html=True)
    
    # Video if available
    if meal.get("strYoutube") and meal["strYoutube"] not in ["null", "", None]:
        st.markdown('<h3 class="section-header">Video Tutorial</h3>', unsafe_allow_html=True)
        try:
            youtube_id = meal["strYoutube"].split("v=")[1]
            st.video(f"https://www.youtube.com/watch?v={youtube_id}")
        except:
            st.markdown(f'<p>Video available at: <a href="{meal["strYoutube"]}" target="_blank">{meal["strYoutube"]}</a></p>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    st.set_page_config(
        page_title="Gourmet Recipe Finder",
        page_icon="🍽️",
        layout="wide"
    )
    run()
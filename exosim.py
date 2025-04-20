# Vincent Vordtriede
# ASTR 191 Big Project - Exoplanet Habitability Simulation
# Note -- run in browser by running this command in the terminal: streamlit run "C:\Users\Vincent\Exosim\exosim.py" 
import math
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.lines as mlines
import numpy as np

def get_albedo(planet_type): #estimate the albedo of the planet based on similarity to known planets
    if planet_type == "Terrestrial":
        return 0.3 #terrestrial--absorbs more light
    elif planet_type == "Neptunian":
        return 0.7 #Ice giant--reflects most light
    elif planet_type == "Jovian":
        return 0.5 #Jovian/gas giant--absorbs half of the star's light
    else:
        return 0.5 #Rough estimate for extreme cases

def in_habitable_zone(luminosity, albedo, distance): #returns True if the planet is in HZ, and False if not
    T_inner = 316  # Inner boundary temperature in Kelvin
    T_outer = 198  # Outer boundary temperature in Kelvin
    sigma = 5.670e-8 #Stefan-Boltzmann Constant

    d_inner = math.sqrt(((1 - albedo) * luminosity) / (T_inner**4 * 16 * math.pi * sigma))
    d_outer = math.sqrt(((1 - albedo) * luminosity) / (T_outer**4 * 16 * math.pi * sigma))

    return d_inner, d_outer, d_inner <= distance <= d_outer

def get_planet_composition(mass, radius): #returns the planet's most likely composition
    M_e = 5.97219e24 #one earth mass in kg
    R_e = 6.378e6 #one earth radius in meters

    if mass < 9.5*M_e and radius < 3*R_e:
        return "Terrestrial"
    
    elif 9.5*M_e < mass < 130*M_e and 3*R_e < radius < 10*R_e:
        return "Neptunian" 
    
    elif mass > 130*M_e and radius > 10*R_e:
        return "Jovian"
    
    else:
        return "Unkown" #For extreme cases

def is_habitable(in_HZ, planet_type):
    if planet_type == "Terrestrial" and in_HZ:
        return "1"
    elif planet_type == "Terrestrial" and not in_HZ:
        return "2"
    elif planet_type == "Neptunian" and in_HZ:
        return "3"
    elif planet_type == "Neptunian" and not in_HZ:
        return "4"
    elif planet_type == "Jovian" and in_HZ:
        return "5"
    elif planet_type == "Jovian" and not in_HZ:
        return "6"
    else:
        return "7"


# Streamlit UI

st.set_page_config(layout="wide")

# st.markdown("""
#     <style>
#         .block-container {
#             padding-top: 0rem;
#         }
#     </style>
# """, unsafe_allow_html=True)

# st.set_page_config(layout="wide")
st.title("Exoplanet Habitability Simulator")

col1, col2 = st.columns([1,1])

with col1:
    st.write("Play around with the sliders to see how the habitable zone changes!")
    mass = st.slider("Planet Mass (M⊕)", min_value=0.0, max_value=1000.0, value=1.0, step=0.01, key="mass")
    radius = st.slider("Planet Radius (R⊕)", min_value=0.0, max_value=20.0, value=1.0, step=0.01, key="radius")
    distance = st.slider("Orbital Distance (AU)", min_value=0.0, max_value=50.0, value=1.0, step=0.01, key="distance")
    luminosity = st.slider("Stellar Luminosity (L☉)", min_value=0.0, max_value=500.0, value=1.0, step=0.01, key="luminosity")

    #Convert to SI units
    mass_inkg = mass*5.972e24
    radius_inm = radius*6.378e6
    distance_inm = distance*1.496e11
    luminosity_inw = luminosity*3.827e+26

    composition = get_planet_composition(mass_inkg, radius_inm)
    albedo = get_albedo(composition)
    d_inner, d_outer, in_HZ = in_habitable_zone(luminosity_inw, albedo, distance_inm)
    final_answer = is_habitable(in_HZ, composition)

    st.subheader("Results")
    if composition == "Terrestrial":
        st.write(f"- **Planet Type:** Terrestrial 🪨")
    elif composition == "Neptunian":
        st.write(f"- **Planet Type:** Neptunian 🧊")
    elif composition == "Jovian":
        st.write(f"- **Planet Type:** Jovian 💨")
    else:
        st.write(f"- **Planet Type:** Unknown ❗")

    st.write(f"- **Habitable Zone:** {d_inner / 1.496e11:.2f} AU to {d_outer / 1.496e11:.2f} AU")

    if in_HZ:
        st.success("Your planet is within it's habitable zone!")
    else:
        st.error("Your planet is outside it's habitable zone.")

    if final_answer == "1":
        st.success("Your Terrestrial planet can likely foster liquid water and is habitable!")
    elif final_answer == "2":
        st.error("Your Terrestrial planet experiences too extreme of temperatures to foster liquid water and is likely not habitable.")
    elif final_answer == "3":
        st.error("Despite being in it's habitable zone, your Neptunian planet experiences too extreme of temperatures to foster liquid water and is likely not habitable.")
    elif final_answer == "4":
        st.error("Your Neptunian planet experiences too extreme of temperatures to foster liquid water and is likely not habitable.")
    elif final_answer == "5":
        st.error("Despite being in it's habitable zone, your Jovian planet experiences too extreme of temperatures to foster liquid water and is likely not habitable.")
    elif final_answer == "6":
        st.error("Your Jovian planet experiences too extreme of temperatures to foster liquid water and is likely not habitable.")
    elif final_answer == "7":
        st.error("Your planet's composition is unknown, making it likely not habitable.")


with col2:
    # Create figure
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.tick_params(axis='both', which='both', labelsize=6)
    ax.set_xlabel("Orbital Distance (AU)", fontsize=8)


    # Draw the habitable zone as a green ring
    hz_outer = patches.Circle((0, 0), d_outer / 1.496e11, color='green', alpha=0.3)
    hz_inner = patches.Circle((0, 0), d_inner / 1.496e11, color='black', alpha=1.0)
    ax.add_patch(hz_outer)
    ax.add_patch(hz_inner)

    #Draw refrence planet orbits
    mercury_orbit = patches.Circle((0, 0), 0.39, edgecolor='white', facecolor='none', linewidth = 0.5, alpha=1.0)
    ax.add_patch(mercury_orbit)

    venus_orbit = patches.Circle((0, 0), 0.723, edgecolor='white', facecolor='none', linewidth = 0.5, alpha=1.0)
    ax.add_patch(venus_orbit)

    earth_orbit = patches.Circle((0, 0), 1, edgecolor='white', facecolor='none', linewidth = 0.5, alpha=1.0)
    ax.add_patch(earth_orbit)

    mars_orbit = patches.Circle((0, 0), 1.524, edgecolor='white', facecolor='none', linewidth = 0.5, alpha=1.0)
    ax.add_patch(mars_orbit)

    jupiter_orbit = patches.Circle((0, 0), 5.20, edgecolor='white', facecolor='none', linewidth = 0.5, alpha=1.0)
    ax.add_patch(jupiter_orbit)

    saturn_orbit = patches.Circle((0, 0), 9.54, edgecolor='white', facecolor='none', linewidth = 0.5, alpha=1.0)
    ax.add_patch(saturn_orbit)

    uranus_orbit = patches.Circle((0, 0), 19.19, edgecolor='white', facecolor='none', linewidth = 0.5, alpha=1.0)
    ax.add_patch(uranus_orbit)

    neptune_orbit = patches.Circle((0, 0), 30.1, edgecolor='white', facecolor='none', linewidth = 0.5, alpha=1.0)
    ax.add_patch(neptune_orbit)

    #handles dynamic resizing and labels
    if distance <2:
        ax.set_xlim(-2,2) #resize the plot
        ax.set_ylim(-2,2)
        ax.set_aspect('equal')

        mercury_label = ax.text(0.0, -0.45, "Mercury orbit", color='white', fontsize=5, verticalalignment='center', horizontalalignment='center') #add neccessary planet labels if in view
        venus_label = ax.text(0.0, -0.8, "Venus orbit", color='white', fontsize=5, verticalalignment='center', horizontalalignment='center')
        earth_label = ax.text(0.0, -1.1, "Earth orbit", color='white', fontsize=5, verticalalignment='center', horizontalalignment='center')
        mars_label = ax.text(0.0, -1.63, "Mars orbit", color='white', fontsize=5, verticalalignment='center', horizontalalignment='center')
        if d_inner / 1.496e11 >math.sqrt(2*((2)**2)): #add the HZ label if it is out of view (using pythagorean theorem to find the radius of the circle)
            hz_label = ax.text(2.0,2.0/5.0, "Habitable \n Zone ➡ ",color='green', fontsize=5, fontweight='bold', verticalalignment='center', horizontalalignment='right')

    elif 2<distance<5:
        buffer = 1  # Adds extra space around the plot
        ax.set_xlim(-distance - buffer, distance + buffer)
        ax.set_ylim(-distance - buffer, distance + buffer)
        ax.set_aspect('equal') # make sure the HZ is a perfect circle
        
        mercury_label = ax.text(0.0, -0.45, "Mercury orbit", color='white', fontsize=5, verticalalignment='center', horizontalalignment='center')
        venus_label = ax.text(0.0, -0.8, "Venus orbit", color='white', fontsize=5, verticalalignment='center', horizontalalignment='center')
        earth_label = ax.text(0.0, -1.1, "Earth orbit", color='white', fontsize=5, verticalalignment='center', horizontalalignment='center')
        mars_label = ax.text(0.0, -1.63, "Mars orbit", color='white', fontsize=5, verticalalignment='center', horizontalalignment='center')
        if d_inner / 1.496e11 >math.sqrt(2*((distance + buffer)**2)): #add the HZ label if it is out of view
            hz_label = ax.text(distance + buffer,(distance + buffer)/5, "Habitable \n Zone ➡ ",color='green', fontsize=5, fontweight='bold',verticalalignment='center', horizontalalignment='right')

    elif 5<distance<10:
        buffer = 2  
        ax.set_xlim(-distance - buffer, distance + buffer)
        ax.set_ylim(-distance - buffer, distance + buffer)
        ax.set_aspect('equal')

        mars_label = ax.text(0.0, -1.63, "Mars orbit", color='white', fontsize=5, verticalalignment='center', horizontalalignment='center')
        jupiter_label = ax.text(0.0, -5.5, "Jupiter orbit", color='white', fontsize=5, verticalalignment='center', horizontalalignment='center')
        if d_inner / 1.496e11 >math.sqrt(2*((distance + buffer)**2)): #add the HZ label if it is out of view
            hz_label = ax.text(distance + buffer,(distance + buffer)/5, "Habitable \n Zone ➡ ",color='green', fontsize=5, fontweight='bold',verticalalignment='center', horizontalalignment='right')

    elif 10<distance<20:
        buffer = 4  
        ax.set_xlim(-distance - buffer, distance + buffer)
        ax.set_ylim(-distance - buffer, distance + buffer)
        ax.set_aspect('equal')

        mars_label = ax.text(0.0, -1.63, "Mars orbit", color='white', fontsize=5, verticalalignment='center', horizontalalignment='center')
        jupiter_label = ax.text(0.0, -5.5, "Jupiter orbit", color='white', fontsize=5, verticalalignment='center', horizontalalignment='center')
        saturn_label = ax.text(0.0, -10.0, "Saturn orbit", color='white', fontsize=5, verticalalignment='center', horizontalalignment='center')
        if d_inner / 1.496e11 >math.sqrt(2*((distance + buffer)**2)): #add the HZ label if it is out of view
            hz_label = ax.text(distance + buffer,(distance + buffer)/5, "Habitable \n Zone ➡ ",color='green', fontsize=5, fontweight='bold',verticalalignment='center', horizontalalignment='right')

    elif 20<distance<30:
        buffer = 6  
        ax.set_xlim(-distance - buffer, distance + buffer)
        ax.set_ylim(-distance - buffer, distance + buffer)
        ax.set_aspect('equal')

        jupiter_label = ax.text(0.0, -5.5, "Jupiter orbit", color='white', fontsize=5, verticalalignment='center', horizontalalignment='center')
        saturn_label = ax.text(0.0, -10.0, "Saturn orbit", color='white', fontsize=5, verticalalignment='center', horizontalalignment='center')
        uranus_label = ax.text(0.0, -19.8, "Uranus orbit", color='white', fontsize=5, verticalalignment='center', horizontalalignment='center')
        if d_inner / 1.496e11 >math.sqrt(2*((distance + buffer)**2)): #add the HZ label if it is out of view
            hz_label = ax.text(distance + buffer,(distance + buffer)/5, "Habitable \n Zone ➡ ",color='green', fontsize=5, fontweight='bold',verticalalignment='center', horizontalalignment='right')

    elif 30<distance<=50:
        buffer = 10  
        ax.set_xlim(-distance - buffer, distance + buffer)
        ax.set_ylim(-distance - buffer, distance + buffer)
        ax.set_aspect('equal')

        jupiter_label = ax.text(0.0, -5.5, "Jupiter orbit", color='white', fontsize=5, verticalalignment='center', horizontalalignment='center')
        saturn_label = ax.text(0.0, -10.0, "Saturn orbit", color='white', fontsize=5, verticalalignment='center', horizontalalignment='center')
        uranus_label = ax.text(0.0, -19.8, "Uranus orbit", color='white', fontsize=5, verticalalignment='center', horizontalalignment='center')
        neptune_label = ax.text(0.0, -31.0, "Neptune orbit", color='white', fontsize=5, verticalalignment='center', horizontalalignment='center')
        if d_inner / 1.496e11 >math.sqrt(2*((distance + buffer)**2)): #add the HZ label if it is out of view
            hz_label = ax.text(distance + buffer,(distance + buffer)/5, "Habitable \n Zone ➡ ",color='green', fontsize=5, fontweight='bold',verticalalignment='center', horizontalalignment='right')


    # Draw the star (yellow circle at origin)
    ax.scatter(0, 0, color='yellow', s=50, label="Star")

    # Draw the planet at its orbital distance
    ax.scatter(distance, 0, color='blue', s=10, label="Planet")
    #draw planet's orbit
    exoplanet_orbit = patches.Circle((0, 0), distance, edgecolor='blue', facecolor='none', linewidth = 0.5, alpha=0.5)
    ax.add_patch(exoplanet_orbit)

    ax.set_xlabel("Orbital Distance (AU)")
    # Create custom legend handles
    habitable_patch = patches.Patch(color='green', alpha=0.3, label="Habitable Zone")
    star = mlines.Line2D([], [], color='yellow', marker='o', linestyle='None', markersize=8, label="Star")
    planet = mlines.Line2D([], [], color='blue', marker='o', linestyle='None', markersize=4, label="Planet")
    ax.legend(handles=[star, planet, habitable_patch], loc="upper right", bbox_to_anchor=(1, 1), fontsize = 8)
    
    # Display plot in Streamlit
    st.pyplot(fig)


#Non-streamlit output
# def main():
#     print("Welcome to the Exoplanet Habitability Simulator!")
#     print("================================================")
#     user_mass = float(input("Enter the mass of your planet (in kg): "))
#     print("================================================")
#     user_radius = float(input("Enter the radius of your planet (in meters): "))
#     print("================================================")
#     user_distance = float(input("Enter the distance of your planet from it's host star (in meters): "))
#     print("================================================")
#     user_luminosity = float(input("Enter the luminosity of your planet's host star (in watts): "))
#     print("================================================")
    
#     user_planet_composition = get_planet_composition(user_mass, user_radius)
#     user_albedo = get_albedo(user_planet_composition)

#     in_HZ = in_habitable_zone(user_luminosity, user_albedo, user_distance)
#     if in_HZ:
#         print(f"Your planet's composition is likely {user_planet_composition} and lies within it's calculated habitable zone.")
#     else:
#         print(f"Your planet's composition is likely {user_planet_composition} and does not lie within it's calculated habitable zone.")
# main()
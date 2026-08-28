import ipaddress
import streamlit as st

st.set_page_config(page_title="Subnet Calculator", page_icon="🌐")

st.title("🌐 Network Subnet Calculator")
st.write("Enter an IP address and CIDR prefix to calculate subnet details.")

# User inputs via visual form fields
ip_input = st.text_input("IP Address", value="192.168.1.1")
prefix_input = st.text_input("Subnet Bits (e.g. 24 or /24)", value="24")

if st.button("Calculate Subnet"):
    prefix = prefix_input.lstrip("/")

    try:
        cidr_str = f"{ip_input}/{prefix}"
        net = ipaddress.IPv4Network(cidr_str, strict=False)
        total_ips = net.num_addresses

        if total_ips > 2:
            usable_ips_count = total_ips - 2
            first_host = net.network_address + 1
            last_host = net.broadcast_address - 1
            host_range = f"{first_host} - {last_host}"
        elif total_ips == 2:
            usable_ips_count = 2
            host_range = f"{net[0]} - {net[1]}"
        else:
            usable_ips_count = 1
            host_range = f"{net.network_address}"

        st.success("Subnet Calculated Successfully!")

        col1, col2 = st.columns(2)
        with col1:
            st.metric(
                "Network Address", f"{net.network_address}/{net.prefixlen}"
            )
            st.metric("Subnet Mask", str(net.netmask))
            st.metric("Total IPs", total_ips)
        with col2:
            st.metric("Usable Host IPs", usable_ips_count)
            st.metric("Broadcast Address", str(net.broadcast_address))

        st.info(f"**Usable IP Range:** {host_range}")

    except ValueError as e:
        st.error(f"Invalid input: {e}")

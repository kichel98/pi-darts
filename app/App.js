import { StatusBar } from 'expo-status-bar';
import React, {useEffect, useState} from 'react';
import { StyleSheet, Text, View } from 'react-native';
import Svg, { G, Circle, Path } from "react-native-svg"

export default function App() {
  const [segment, setSegment] = useState("not detected");
  useEffect(() => {
    const socket = new WebSocket('ws://192.168.1.52:4321');
    socket.onopen = () => {
      console.log("opened!")
    };
    socket.onopen = () => {
      console.log("closed!")
    };
    socket.onmessage = e => {
      console.log(segment);
      setSegment(e.data);
    };
  }, []);
  // converted from assets/tarcza_kontury.svg by https://react-svgr.com/playground/?native=true
  return (
    <View style={styles.container}>
      <Svg
        xmlns="http://www.w3.org/2000/svg"
        width="100%"
        height="50%"
        viewBox="0 0 50 50"
      >
        <G fill="none" stroke="#000">
          <Circle cx={25} cy={25} r={22.5} strokeWidth={0.09} />
          <Circle cx={25} cy={25} r={17} strokeWidth={0.09} />
          <Circle cx={25} cy={25} r={16.2} strokeWidth={0.09} />
          <Circle cx={25} cy={25} r={10.74} strokeWidth={0.09} />
          <Circle cx={25} cy={25} r={9.94} strokeWidth={0.09} />
          <Circle cx={25} cy={25} r={1.59} strokeWidth={0.09} />
          <Circle cx={25} cy={25} r={0.635} strokeWidth={0.09} />
          <Circle cx={36.8} cy={29} r={0.8} fill="red" strokeWidth={0} />
          <Path
            d="M26.57 25.249l15.22 2.41M26.417 25.722l13.73 6.996M26.124 26.124l10.897 10.897M25.722 26.417l6.996 13.73M25.249 26.57l2.41 15.22M24.751 26.57l-2.41 15.22M24.278 26.417l-6.996 13.73M23.876 26.124L12.979 37.021M23.583 25.722l-13.73 6.996M23.43 25.249l-15.22 2.41M23.43 24.751l-15.22-2.41M23.583 24.278l-13.73-6.996M23.876 23.876L12.979 12.979M24.278 23.583l-6.996-13.73M24.751 23.43l-2.41-15.22M25.249 23.43l2.41-15.22M25.722 23.583l6.996-13.73M26.124 23.876l10.897-10.897M26.417 24.278l13.73-6.996M26.57 24.751l15.22-2.41"
            strokeWidth={0.09}
          />
        </G>
      </Svg>
      <Text style={{ fontSize: 20 }}>Punkty za ostatni rzut: {segment}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
});

import React, {useEffect, useState} from 'react';
import { StyleSheet, Text, View } from 'react-native';
import {registerRootComponent} from "expo";
import Dartboard from "./components/Dartboard";
import WebSocketClient from "./helpers/WebSocketClient";

export default function App() {
  const [segment, setSegment] = useState("");

  useEffect(() => {
    const wsClient = new WebSocketClient();
    wsClient.setSetterOnMessage(setSegment);
  }, []);

  return (
    <View style={styles.container}>
      <Dartboard/>
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

registerRootComponent(App);

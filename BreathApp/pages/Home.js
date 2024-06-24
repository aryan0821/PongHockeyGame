import React, { useRef, useEffect, useState } from 'react';
import { Animated, Dimensions, Easing, StyleSheet, View, Text, TouchableOpacity } from 'react-native';

const { width } = Dimensions.get('window');
const circleSize = width / 3;

const Home = () => {
  const move = useRef(new Animated.Value(0)).current;
  const breathIn = Easing.out(Easing.sin);
  const breathOut = Easing.in(Easing.sin);
  const [timer, setTimer] = useState(60);
  const [isPaused, setIsPaused] = useState(false);
  const countdown = useRef(null);
  const animationLoop = useRef(null);

  useEffect(() => {
    startAnimation();
    startTimer();

    return () => {
      clearInterval(countdown.current);
      move.stopAnimation();
    };
  }, []);

  useEffect(() => {
    if (isPaused) {
      clearInterval(countdown.current);
      move.stopAnimation();
    } else {
      startTimer();
      startAnimation();
    }
  }, [isPaused]);

  const startAnimation = () => {
    animationLoop.current = Animated.loop(
      Animated.sequence([
        Animated.timing(move, {
          toValue: 1,
          duration: 7000, // 7 seconds for breath in
          easing: breathIn,
          useNativeDriver: true,
        }),
        Animated.timing(move, {
          toValue: 2,
          duration: 7000, // 7 seconds for breath out
          easing: breathOut,
          useNativeDriver: true,
        }),
        Animated.timing(move, {
          toValue: 0.0,
          duration: 0,
          useNativeDriver: true,
        }),
      ]),
    );
    animationLoop.current.start();
  };

  const startTimer = () => {
    clearInterval(countdown.current); // Clear any existing interval
    countdown.current = setInterval(() => {
      setTimer((prev) => (prev > 0 ? prev - 1 : prev));
    }, 1000);
  };

  const handleReset = () => {
    setTimer(60);
    setIsPaused(false);
    clearInterval(countdown.current);
    move.stopAnimation(() => {
      move.setValue(0); // Reset the animation to its start position
      startTimer();
      startAnimation();
    });
  };

  const handlePause = () => {
    setIsPaused((prev) => !prev);
  };

  const translate = move.interpolate({
    inputRange: [0, 1, 2],
    outputRange: [0, circleSize / 6, 0],
  });

  return (
    <View style={styles.container}>
      <View style={styles.leftContainer}>
        <View style={styles.circlesContainer}>
          {[0, 1, 2, 3, 4, 5, 6, 7].map((item) => {
            const rotation = move.interpolate({
              inputRange: [0, 1, 2],
              outputRange: [
                `${item * 45}deg`,
                `${item * 45 + 180}deg`,
                `${item * 45 + 360}deg`,
              ],
            });
            return (
              <View
                key={item}
                style={{
                  ...StyleSheet.absoluteFill,
                  alignItems: 'center',
                  justifyContent: 'center',
                }}>
                <Animated.View
                  style={{
                    opacity: 0.15,
                    backgroundColor: '#d600d3',
                    width: circleSize,
                    height: circleSize,
                    borderRadius: circleSize / 2,
                    transform: [
                      {
                        rotateZ: rotation,
                      },
                      { translateX: translate },
                      { translateY: translate },
                    ],
                  }}
                />
              </View>
            );
          })}
          <Animated.View
            style={{
              position: 'absolute',
              alignItems: 'center',
              justifyContent: 'center',
              opacity: move.interpolate({
                inputRange: [0, 1, 1.5, 2],
                outputRange: [1, 1, 0, 0],
              }),
            }}
          >
            <Text style={styles.text}>Inhale</Text>
          </Animated.View>
          <Animated.View
            style={{
              position: 'absolute',
              alignItems: 'center',
              justifyContent: 'center',
              opacity: move.interpolate({
                inputRange: [0, 1, 1.5, 2],
                outputRange: [0, 0, 1, 1],
              }),
            }}
          >
            <Text style={styles.text}>Exhale</Text>
          </Animated.View>
        </View>
      </View>
      <View style={styles.rightContainer}>
        <View style={styles.buttonContainer}>
          <TouchableOpacity onPress={handleReset} style={styles.button}>
            <Text style={styles.buttonText}>Restart</Text>
          </TouchableOpacity>
          <TouchableOpacity onPress={handlePause} style={styles.button}>
            <Text style={styles.buttonText}>{isPaused ? "Measure" : "Stop"}</Text>
          </TouchableOpacity>
        </View>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    flexDirection: 'row',
    backgroundColor: '#0000',
    marginTop: 10,
    marginBottom: 0,
    width: '80%',
  },
  leftContainer: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
  },
  rightContainer: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
  },
  circlesContainer: {
    ...StyleSheet.absoluteFill,
    alignItems: 'center',
    justifyContent: 'center',
  },
  text: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#d600d3',
  },
  buttonContainer: {
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'space-around',
    height: '40%',
  },
  button: {
    backgroundColor: '#d600d3',
    width: 100,
    padding: 7,
    borderRadius: 5,
    marginVertical: 10,
  },
  buttonText: {
    fontSize: 18,
    color: '#fff',
    fontWeight: 'bold',
    textAlign: 'center',
  },
});

export default Home;
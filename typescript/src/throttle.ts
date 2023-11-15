interface Duration {
  value: number
  unit: "ms" | "s"
}

function durationToMs(duration: Duration): number {
  return duration.unit === "ms" ? duration.value : duration.value * 1000
}

async function* throttle<T>(input: AsyncIterable<T>, duration: Duration): AsyncIterable<T> {
  // Consume the stream but use a Promise in between `yield` to simulate throttling
  for await (const res of input) {
    await new Promise(resolve => setTimeout(resolve, durationToMs(duration)))
    yield res
  }
}

export default throttle

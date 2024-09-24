import { useState } from "react";
import { Link } from "react-router-dom";
import { ArrowUpRight } from "lucide-react";

const Signup = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [registrationStatus, setRegistrationStatus] = useState(null);

  const handleSignup = async (e) => {
    e.preventDefault();

    const userData = {
      email,
      password,
    };

    try {
      const response = await fetch("https://dev.neucron.io/v1/auth/signup", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(userData),
      });

      if (response.ok) {
        setRegistrationStatus("success");
      } else {
        setRegistrationStatus("error");
      }
    } catch (error) {
      console.error("An error occurred:", error);
      setRegistrationStatus("error");
    }
  };

  return (
    <div className="flex items-center justify-center h-screen bg-[#121212]">
      <div className="w-full max-w-sm p-6 bg-[#1e1e1e] rounded-lg shadow-md">
        <h2 className="text-center text-2xl font-bold text-white">Sign up to create account</h2>
        <p className="mt-2 text-center text-base text-gray-400">
          Already have an account?{" "}
          <Link to="/auth/login" className="font-medium text-green-500 transition-all duration-200 hover:underline">
            Log In
          </Link>
        </p>
        <form onSubmit={handleSignup} className="mt-8">
          <div className="space-y-5">
            <div>
              <label htmlFor="email" className="text-base font-medium text-gray-300">Email address</label>
              <div className="mt-2">
                <input
                  className="flex h-10 w-full rounded-md border border-gray-600 bg-[#2a2a2a] text-white placeholder-gray-400 focus:outline-none focus:ring-1 focus:ring-green-600"
                  type="email"
                  placeholder="Enter your email"
                  id="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                />
              </div>
            </div>
            <div>
              <label htmlFor="password" className="text-base font-medium text-gray-300">Password</label>
              <div className="mt-2">
                <input
                  className="flex h-10 w-full rounded-md border border-gray-600 bg-[#2a2a2a] text-white placeholder-gray-400 focus:outline-none focus:ring-1 focus:ring-green-600"
                  type="password"
                  placeholder="Enter your password"
                  id="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />
              </div>
            </div>
            <div>
              <button
                type="submit"
                className="inline-flex w-full items-center justify-center rounded-md bg-green-600 px-3.5 py-2.5 font-semibold leading-7 text-white hover:bg-green-500"
              >
                Create Account <ArrowUpRight className="ml-2" size={16} />
              </button>
            </div>
            {registrationStatus === "success" && (
              <p className="text-green-400 text-center">Registration successful!</p>
            )}
            {registrationStatus === "error" && (
              <p className="text-red-400 text-center">Registration failed. Please try again.</p>
            )}
          </div>
        </form>
      </div>
    </div>
  );
};

export default Signup;
